import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import translate_v3
from google.cloud.translate_v3.proto.translation_service_pb2 import (
    SupportedLanguages,
    SupportedLanguage,
    TranslateTextResponse,
    Translation,
)

from engines import BaseTranslationEngine
from errors import (
    TranslationEngineNotConfiguredError,
    AlignmentNotSupportedError,
    EngineApiError,
    InvalidISO6391CodeError,
    DetectionError,
    TranslationError,
)
from models import TranslationResponse
from settings import Settings


def bcp_47_to_iso_639(bcp_47_code: str):
    code = bcp_47_code.split("-")[0]
    if len(code) == 2:
        return code
    if len(code) == 3:
        raise InvalidISO6391CodeError(
            f"BCP-47 code: {bcp_47_code} could not be converted. "
            f"3-letter ISO-639 language codes are not supported"
        )
    raise InvalidISO6391CodeError(
        f"BCP-47 code: {bcp_47_code} could not be converted as has no ISO-639 component"
    )


class GoogleEngine(BaseTranslationEngine):
    NAME = "google"
    VERSION = "3"

    supports_detection = True

    def __init__(self):
        settings = Settings()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(settings.log_level.value)
        # todo: use endpoint with client options kwarg in initialization of client
        self.endpoint = settings.google_endpoint
        if settings.google_svc_account_json_path is None:
            raise TranslationEngineNotConfiguredError(
                f"{self.name_ver} engine: no service account json path configured"
            )
        self.client = self.get_client(settings.google_svc_account_json_path)
        if settings.google_parent_path is None:
            raise TranslationEngineNotConfiguredError(
                f"{self.name_ver} engine: parent path not configured"
            )
        self.parent = str(settings.google_parent_path)
        super().__init__()

    def get_client(self, path: Path):
        try:
            return translate_v3.TranslationServiceClient.from_service_account_file(
                str(path)
            )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise TranslationEngineNotConfiguredError(
                f"{self.name_ver} engine: invalid service account json"
            ) from e

    def get_supported_translations(self) -> Dict[str, List[str]]:
        try:
            supported_languages: SupportedLanguages = self.client.get_supported_languages(
                parent=self.parent
            )
        except GoogleAPICallError as e:
            raise EngineApiError(
                f"{self.name_ver} had a problem making get supported languages api request"
            ) from e
        # todo: make supported languages list a set
        languages: List[SupportedLanguage] = supported_languages.languages
        all_codes = [language.language_code.split("-")[0] for language in languages]
        return {c: all_codes for c in all_codes}

    async def translate(
        self,
        source_text: str,
        to_language: str,
        from_language: Optional[str] = None,
        with_alignment: Optional[bool] = False,
    ) -> TranslationResponse:
        await super().translate(source_text=source_text, to_language=to_language, from_language=from_language,
                                with_alignment=with_alignment)
        # todo: support other mime types
        try:
            translated_text: TranslateTextResponse = self.client.translate_text(
                contents=[source_text],
                target_language_code=to_language,
                source_language_code=from_language,
                parent=self.parent,
                mime_type="text/plain",
            )
        except GoogleAPICallError as e:
            raise EngineApiError(
                f"{self.name_ver} had a problem making translate api request"
            ) from e
        translations: List[Translation] = translated_text.translations
        translation = translations[0]
        self._logger.debug("%s got response: %s", self.name_ver, translation)

        detected_language_confidence = detected_language = None

        if from_language is None:
            try:
                detected_language = bcp_47_to_iso_639(
                    translation.detected_language_code
                )
            except (InvalidISO6391CodeError, AttributeError) as e:
                raise DetectionError(
                    f"{self.name_ver} engine could not detect which language the source text is in"
                ) from e

        try:
            translated_text = translation.translated_text
        except AttributeError as e:
            raise TranslationError(
                f"{self.name_ver} engine could not translate the given text"
            ) from e

        return TranslationResponse(
            engine=self.NAME,
            engine_version=self.VERSION,
            source_text=source_text,
            from_language=from_language or detected_language,
            to_language=to_language,
            detected_language_confidence=detected_language_confidence,
            translated_text=translated_text,
            alignment=None,
        )
