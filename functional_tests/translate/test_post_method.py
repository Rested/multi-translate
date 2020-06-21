import httpx

from functional_tests.translate.test_translate import translate_url


def test_post_method():
    request_data = {
        "from_language": "en",
        "to_language": "es",
        "source_text": "hello",
        "preferred_engine": "microsoft",
        "with_alignment": False,
    }
    resp = httpx.post(translate_url(), json=request_data)
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