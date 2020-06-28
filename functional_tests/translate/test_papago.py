import httpx

from functional_tests.translate.test_translate import translate_url


def test_translate_papago_basic():
    request_data = {
        "from_language": "en",
        "to_language": "ko",
        "source_text": "hello",
        "preferred_engine": "papago",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "안녕하십니까",
        "engine": "papago",
        "engine_version": "1",
        "from_language": "en",
        "to_language": "ko",
        "source_text": "hello",
        "detected_language_confidence": None,
        "alignment": None,
    }


def test_translate_papago_detection():
    request_data = {
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "papago",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 400
    result = resp.json()
    assert result == {
        "detail": "papago (1) engine does not support detection, please specify from_language"
    }


def test_translate_papago_alignment():
    request_data = {
        "from_language": "en",
        "to_language": "ko",
        "source_text": "hello",
        "preferred_engine": "papago",
        "with_alignment": True,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 400
    result = resp.json()
    assert result == {
        "detail": "papago (1) does not support alignment",
    }


def test_is_best_for_korean():
    request_data = {
        "from_language": "en",
        "to_language": "ko",
        "source_text": "hello",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "안녕하십니까",
        "engine": "papago",
        "engine_version": "1",
        "from_language": "en",
        "to_language": "ko",
        "source_text": "hello",
        "detected_language_confidence": None,
        "alignment": None,
    }


def test_will_fallback_when_papago_does_not_support_language_pair():
    request_data = {
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "with_alignment": False,
        "fallback": True,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()
    assert result == {
        "translated_text": "hola",
        "engine": "deepl",
        "engine_version": "2",
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "detected_language_confidence": None,
        "alignment": None,
    }
