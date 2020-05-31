import httpx

from functional_tests.translate.test_translate import translate_url


def test_translate_microsoft_basic():
    request_data = {
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "microsoft",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "Hola",
        "engine": "microsoft",
        "engine_version": "3.0",
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "detected_language_confidence": None,
        "alignment": None,
    }


def test_translate_microsoft_detection():
    request_data = {
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "microsoft",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "Hola",
        "engine": "microsoft",
        "engine_version": "3.0",
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "detected_language_confidence": 1.0,
        "alignment": None,
    }


def test_translate_microsoft_alignment():
    request_data = {
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "microsoft",
        "with_alignment": True,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "Hola",
        "engine": "microsoft",
        "engine_version": "3.0",
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "detected_language_confidence": None,
        "alignment": [
            {
                "dest": {"end": "3", "start": "0", "text": "Hola"},
                "src": {"end": "4", "start": "0", "text": "hello"},
            }
        ],
    }


def test_translate_microsoft_alignment_with_bad_pair():
    request_data = {
        "from_language": "es",
        "to_language": "fr",
        "source_text": "hola",
        "preferred_engine": "microsoft",
        "with_alignment": True,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 400
    result = resp.json()
    assert result == {
        "detail": "microsoft (3.0) engine does not support alignment between es and fr"
    }
