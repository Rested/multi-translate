from urllib.parse import urljoin

import httpx
import requests
import trio
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from functional_tests.ft_settings import FTSettings

base = FTSettings().rest_url

query = gql(
    """
query GetTranslation {
    translation(sourceText: "How do you do?", toLanguage: "es", withAlignment: true) {
        translatedText
        fromLanguage
        alignment{
          src{
            start,
            end,
            text
          }
          dest{
            start,
            end,
            text
          }
        }
  }
}
"""
)


def test_graphql_works():
    transport = RequestsHTTPTransport(
        url=urljoin(base, "gql"), verify=False, retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True, )

    result = client.execute(query)

    assert result == {
        "translation": {
            "translatedText": "¿Cómo estás?",
            "fromLanguage": "en",
            "alignment": [
                {
                    "src": {"start": "0", "end": "13", "text": "How do you do?"},
                    "dest": {"start": "0", "end": "11", "text": "¿Cómo estás?"},
                }
            ],
        }
    }


async def check_rate_limit(client, i, results):
    await trio.sleep((1. / 40.) * i)
    try:
        result = client.execute(query)
    except requests.exceptions.HTTPError as e:
        result = str(e)
    if "translation" in result:
        results[i] = 200
    if "429" in result:
        results[i] = 429


async def test_gql_rate_limits():
    await trio.sleep(2)
    transport = RequestsHTTPTransport(
        url=urljoin(base, "gql"), verify=False, retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True, )
    results = {}
    async with trio.open_nursery() as nursery:
        for i in range(40):
            nursery.start_soon(check_rate_limit, client, i, results)
    assert 40 > list(results.values()).count(200) >= 20
    assert 0 < list(results.values()).count(429) <= 20
    await trio.sleep(1)
