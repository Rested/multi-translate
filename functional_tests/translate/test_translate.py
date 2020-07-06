import time
from urllib.parse import urljoin
import trio
import httpx

from functional_tests.ft_settings import FTSettings


def translate_url() -> str:
    base = FTSettings().rest_url
    return urljoin(base, "translate")


def test_translate_basic():
    assert translate_url().endswith("translate")
    resp = httpx.get(translate_url())
    assert resp.status_code == 422


async def check_rate_limit(client, i: int, method="GET"):
    await trio.sleep(0.01 * i)
    data = {
        "to_language": "es",
        "source_text": f"hello",
        "from_language": "en",
    }
    r = await client.request(method, translate_url(), params=data if method == "GET" else None,
                             json=data if method == "POST" else None)
    if i > 40:
        assert r.status_code == 429
    elif i >= 17:
        assert r.status_code in (200, 429)
    else:
        assert r.status_code == 200


async def test_rate_limits():
    await trio.sleep(2)
    async with httpx.AsyncClient() as client:
        async with trio.open_nursery() as nursery:
            for i in range(50):
                nursery.start_soon(check_rate_limit, client, i)
    await trio.sleep(2)


async def test_rate_limits_post():
    await trio.sleep(2)
    async with httpx.AsyncClient() as client:
        async with trio.open_nursery() as nursery:
            for i in range(50):
                nursery.start_soon(check_rate_limit, client, i, "POST")
    await trio.sleep(1)
