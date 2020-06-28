from urllib.parse import urljoin

import httpx

from functional_tests.ft_settings import FTSettings


def translate_url() -> str:
    base = FTSettings().rest_url
    return urljoin(base, "translate")


def test_translate_basic():
    assert translate_url().endswith("translate")
    resp = httpx.get(translate_url())
    assert resp.status_code == 422
