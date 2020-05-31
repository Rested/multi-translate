import httpx

from functional_tests.translate.test_translate import translate_url


def test_translate_google_basic():
    request_data = {
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "google",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "Hola",
        "engine": "google",
        "engine_version": "3",
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "detected_language_confidence": None,
        "alignment": None,
    }


def test_translate_google_detection():
    request_data = {
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "google",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "Hola",
        "engine": "google",
        "engine_version": "3",
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "detected_language_confidence": None,
        "alignment": None,
    }
