import pytest
import yaml

from errors import InvalidLanguagePreferencesError
from engines.controller import _load_language_preferences, _best_engine_by_language, ENGINE_NAME_MAP


def test_load_language_preferences_with_non_existent_file():
    with pytest.raises(InvalidLanguagePreferencesError) as exc_info:
        _load_language_preferences("/tmp/somethingthatdoesntexist.yaml")

    assert "no" in str(exc_info) and "file" in str(exc_info)


def test_load_language_preferences_with_bad_yaml(tmpdir):
    invalid_yaml = """
this: 
  is: 
    - "invalid".
"""
    p = tmpdir.join("language_preferences.yaml")
    with open(p, "w") as f:
        f.write(invalid_yaml)
    with pytest.raises(InvalidLanguagePreferencesError) as exc_info:
        _load_language_preferences(p)

    assert "invalid" in str(exc_info)


def test_load_language_preferences_succeeds_with_default_yaml():
    preferences, default_ordering = _load_language_preferences()
    assert "xx" in preferences
    assert set(default_ordering) == set(ENGINE_NAME_MAP.keys())


def test_load_language_preferences_fails_if_no_default(tmpdir):
    preferences = {
        "xx": {
            "en": ["google", "microsoft"]
        }
    }
    p = tmpdir.join("language_preferences.yaml")
    with open(p, "w") as f:
        yaml.safe_dump(preferences, f)

    with pytest.raises(InvalidLanguagePreferencesError) as exc_info:
        _load_language_preferences(p)

    assert "default" in str(exc_info)


def test_load_language_preferences_fails_if_all_engines_not_in_default(tmpdir):
    preferences = {
        "xx": {
            "xx": ["google", "microsoft"]
        }
    }
    p = tmpdir.join("language_preferences.yaml")
    with open(p, "w") as f:
        yaml.safe_dump(preferences, f)

    with pytest.raises(InvalidLanguagePreferencesError) as exc_info:
        _load_language_preferences(p)

    assert "all" in str(exc_info)
    assert "missing" in str(exc_info)
    assert "amazon" in str(exc_info)


def test_best_engine_by_language_with_only_default():
    ordering = list(ENGINE_NAME_MAP.keys())
    preferences = {
        "xx": {
            "xx": ordering
        }
    }
    best_engine = _best_engine_by_language(engines=ENGINE_NAME_MAP, from_language=None, to_language="en",
                                           language_preferences=preferences, base_ordering=ordering)

    assert ENGINE_NAME_MAP["microsoft"] == best_engine


def test_best_engine_by_language_with_reduced_engines_dict():
    ordering = list(ENGINE_NAME_MAP.keys())
    preferences = {
        "xx": {
            "xx": ordering
        }
    }
    name_map_copy = ENGINE_NAME_MAP.copy()
    del name_map_copy["microsoft"]
    best_engine = _best_engine_by_language(engines=name_map_copy, from_language=None, to_language="en",
                                           language_preferences=preferences, base_ordering=ordering)

    assert ENGINE_NAME_MAP["google"] == best_engine


def test_best_engine_by_language_follows_to_language_preferences_when_specified():
    ordering = list(ENGINE_NAME_MAP.keys())
    preferences = {
        "xx": {
            "xx": ordering,
            "en": ["deepl"]
        }
    }

    best_engine = _best_engine_by_language(engines=ENGINE_NAME_MAP, from_language=None, to_language="en",
                                           language_preferences=preferences, base_ordering=ordering)

    assert ENGINE_NAME_MAP["deepl"] == best_engine


def test_best_engine_by_language_falls_back_to_default_ordering_when_to_language_preferences_engines_are_not_available():
    ordering = list(ENGINE_NAME_MAP.keys())
    preferences = {
        "xx": {
            "xx": ordering,
            "en": ["deepl"]
        }
    }
    name_map_copy = ENGINE_NAME_MAP.copy()
    del name_map_copy["deepl"]
    best_engine = _best_engine_by_language(engines=name_map_copy, from_language=None, to_language="en",
                                           language_preferences=preferences, base_ordering=ordering)

    assert ENGINE_NAME_MAP["microsoft"] == best_engine


def test_best_engine_by_language_follows_from_language_preferences_when_specified():
    ordering = list(ENGINE_NAME_MAP.keys())
    preferences = {
        "xx": {
            "xx": ordering,
        },
        "en": {
            "xx": list(reversed(ordering))
        }
    }
    name_map_copy = ENGINE_NAME_MAP.copy()
    best_engine = _best_engine_by_language(engines=name_map_copy, from_language="en", to_language="es",
                                           language_preferences=preferences, base_ordering=ordering)

    assert ENGINE_NAME_MAP["yandex"] == best_engine


def test_best_engine_by_language_falls_back_to_default_when_to_language_or_any_does_not_exist_in_to_preferences():
    ordering = list(ENGINE_NAME_MAP.keys())
    preferences = {
        "xx": {
            "xx": ordering,
        },
        "en": {
            "fr": ["papago"]
        }
    }
    name_map_copy = ENGINE_NAME_MAP.copy()
    best_engine = _best_engine_by_language(engines=name_map_copy, from_language="en", to_language="es",
                                           language_preferences=preferences, base_ordering=ordering)

    assert ENGINE_NAME_MAP["microsoft"] == best_engine


def test_best_engine_by_language_uses_preferences_when_both_to_and_from_specified_and_available():
    ordering = list(ENGINE_NAME_MAP.keys())
    preferences = {
        "xx": {
            "xx": ordering,
        },
        "kr": {
            "fr": ["papago"]
        }
    }
    best_engine = _best_engine_by_language(engines=ENGINE_NAME_MAP, from_language="kr", to_language="fr",
                                           language_preferences=preferences, base_ordering=ordering)

    assert ENGINE_NAME_MAP["papago"] == best_engine


def test_best_engine_by_language_falls_back_to_default_to_lang_prefs():
    ordering = list(ENGINE_NAME_MAP.keys())
    preferences = {
        "xx": {
            "xx": ordering,
        },
        "kr": {
            "xx": list(reversed(ordering)),
            "fr": ["papago"]
        }
    }
    name_map_copy = ENGINE_NAME_MAP.copy()
    del name_map_copy["papago"]
    best_engine = _best_engine_by_language(engines=name_map_copy, from_language="kr", to_language="fr",
                                           language_preferences=preferences, base_ordering=ordering)

    assert ENGINE_NAME_MAP["yandex"] == best_engine
