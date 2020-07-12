from urllib.parse import urljoin

import httpx

from functional_tests.ft_settings import FTSettings


def test_supported_languages():
    base = FTSettings().rest_url

    url = urljoin(base, "supported-languages")

    resp = httpx.get(url)
    assert resp.status_code == 200
    supported_langs = resp.json()
    assert "en" in supported_langs
    assert "ko" in supported_langs["en"]


def test_available_engines():
    base = FTSettings().rest_url

    url = urljoin(base, "available-engines")

    resp = httpx.get(url)
    assert resp.status_code == 200
    available_engines = resp.json()
    assert "google" in available_engines
    assert "papago" in available_engines
