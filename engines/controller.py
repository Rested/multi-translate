import logging
from typing import Dict, List, Optional, Tuple

import yaml

from engines.amazon import AmazonEngine
from engines.base import BaseTranslationEngine
from engines.deep_l import DeepLEngine
from engines.google import GoogleEngine
from engines.microsoft import MicrosoftEngine
from engines.papago import PapagoEngine
from engines.yandex import YandexEngine
from errors import (
    EngineApiError,
    InvalidEngineNameError,
    InvalidLanguagePreferencesError,
    NoValidEngineConfiguredError,
    TranslationEngineNotConfiguredError,
    UnsupportedLanguagePairError,
)
from settings import Settings


BEST = "best"
SUPPORTED_ENGINES = (
    MicrosoftEngine,
    GoogleEngine,
    AmazonEngine,
    PapagoEngine,
    DeepLEngine,
    YandexEngine,
)
ENGINE_NAME_MAP = {e.NAME: e for e in SUPPORTED_ENGINES}

LangPref = Dict[str, Dict[str, List[str]]]


def _load_language_preferences(
    path: Optional[str] = None,
) -> Tuple[LangPref, List[str]]:
    try:
        with open(path or "language_preferences.yaml", "r") as f:
            preferences = yaml.safe_load(f)
    except FileNotFoundError:
        raise InvalidLanguagePreferencesError("no language preferences file found")
    except yaml.YAMLError:
        raise InvalidLanguagePreferencesError("invalid yaml syntax")

    try:
        ordering = preferences["xx"]["xx"]
    except KeyError:
        raise InvalidLanguagePreferencesError(
            "language preferences yaml must have an xx.xx (default) ordering"
        )

    diff = set(ENGINE_NAME_MAP.keys()) - set(ordering)
    if diff:
        raise InvalidLanguagePreferencesError(
            f"all engines must be included in the default ordering - missing {diff}"
        )
    return preferences, ordering


default_language_preferences, default_ordering = _load_language_preferences()


def _best_engine_by_language(
    engines: Dict[str, BaseTranslationEngine],
    from_language: Optional[str],
    to_language: str,
    language_preferences: LangPref,
    base_ordering: List[str],
) -> BaseTranslationEngine:
    from_l_preferences = language_preferences.get(
        from_language, language_preferences["xx"]
    )

    default_from_language_ordering = from_l_preferences.get("xx", base_ordering)
    specified_ordering = from_l_preferences.get(
        to_language, default_from_language_ordering
    )

    filled_ordering = specified_ordering + [
        engine_name
        for engine_name in default_from_language_ordering
        if engine_name not in specified_ordering
    ]
    filled_ordering += [
        engine_name
        for engine_name in base_ordering
        if engine_name not in filled_ordering
    ]

    return next(
        engines[engine_name]
        for engine_name in filled_ordering
        if engine_name in engines
    )


class EngineController:
    def __init__(self):
        self.available_engines: Dict[str, BaseTranslationEngine] = {}
        settings = Settings()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(settings.log_level.value)
        self._combined_supported_languages = None

    def get_available_engines(self):
        for engine_cls in SUPPORTED_ENGINES:
            try:
                self.available_engines[engine_cls.NAME] = engine_cls()
            except (TranslationEngineNotConfiguredError, EngineApiError):
                self._logger.info(
                    "could not initialize %s engine", engine_cls.NAME, exc_info=True
                )
        self._logger.info(
            "initialized the following engines %s", self.available_engines.keys()
        )

    def get_best(
        self,
        needs_detection: bool,
        needs_alignment: bool,
        from_language: Optional[str],
        to_language: str,
        exclude_engines: List[str],
    ):
        engine_candidates: Dict[str, BaseTranslationEngine] = {}
        for engine_name, engine_instance in self.available_engines.items():
            if engine_name in exclude_engines:
                continue
            if needs_detection and not engine_instance.supports_detection:
                continue
            if needs_alignment and not engine_instance.supports_alignment:
                continue
            try:
                engine_instance.is_language_pair_supported(
                    from_language=from_language, to_language=to_language
                )
            except UnsupportedLanguagePairError:
                continue
            engine_candidates[engine_name] = engine_instance
        if len(engine_candidates):
            return _best_engine_by_language(
                engine_candidates,
                from_language,
                to_language,
                language_preferences=default_language_preferences,
                base_ordering=default_ordering,
            )
        raise NoValidEngineConfiguredError(
            "no configured engine could carry out the request"
        )

    def get_engine(
        self,
        name: str,
        needs_detection: bool,
        needs_alignment: bool,
        from_language: Optional[str],
        to_language: str,
        exclude_engines: Optional[List[str]] = None,
    ):
        if name == BEST:
            return self.get_best(
                needs_detection,
                needs_alignment,
                from_language,
                to_language,
                exclude_engines or [],
            )
        try:
            return self.available_engines[name]
        except KeyError:
            pass

        try:
            return ENGINE_NAME_MAP[name]()
        except KeyError:
            raise InvalidEngineNameError(
                f"engine {name} not supported try one of {ENGINE_NAME_MAP.keys()}"
            )

    @property
    def combined_supported_languages(self):
        if self._combined_supported_languages is not None:
            return self._combined_supported_languages
        combined_supported_languages = {}
        for engine in self.available_engines.values():
            for from_language, to_languages in engine.supported_translations.items():
                if from_language not in combined_supported_languages:
                    combined_supported_languages[from_language] = list(to_languages)
                else:
                    combined_supported_languages[from_language] = list(
                        set(
                            list(to_languages)
                            + list(combined_supported_languages[from_language])
                        )
                    )
        self._combined_supported_languages = combined_supported_languages
        return self._combined_supported_languages
