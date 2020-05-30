import httpx
from functional_tests.ft_settings import FTSettings
from urllib.parse import urljoin


def translate_url() -> str:
    base = FTSettings().rest_url
    return urljoin(base, "translate")


def test_translate_basic():
    assert translate_url().endswith("translate")
    resp = httpx.get(translate_url())
    assert resp.status_code == 422


def test_translate_microsoft():
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
        "alignment": None
    }
