import httpx

from functional_tests.translate.test_translate import translate_url


def test_translate_amazon_basic():
    request_data = {
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "amazon",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "hola",
        "engine": "amazon",
        "engine_version": "2020-04-30",
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "detected_language_confidence": None,
        "alignment": None,
    }


def test_translate_amazon_detection():
    request_data = {
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "amazon",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 400
    result = resp.json()
    assert result == {
        "detail": "amazon (2020-04-30) engine does not support detection, please specify from_language"
    }


def test_translate_amazon_alignment():
    request_data = {
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "amazon",
        "with_alignment": True,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 400
    result = resp.json()
    assert result == {
        "detail": "amazon (2020-04-30) does not support alignment",
    }
