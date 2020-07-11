from urllib.parse import urljoin

import pytest
import requests
import trio
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from functional_tests.ft_settings import FTSettings


base = FTSettings().rest_url

query_str = """
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
query = gql(query_str)


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


def test_max_characters():
    transport = RequestsHTTPTransport(
        url=urljoin(base, "gql"), verify=False, retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True, )

    long_str = "then the more there are the better in order that they neutralize each other. When in the later part of the book he comes to consider government... these three should form a crescendo but usually perform a diminuendo."
    q = query_str.replace("How do you do?", long_str)
    with pytest.raises(Exception) as e:
        _ = client.execute(gql(q))

    assert str(e.value) == str({
        'message': '1 validation error for TranslationRequest\nsource_text\n  ensure this value has at most 200 characters (type=value_error.any_str.max_length; limit_value=200)',
        'locations': [{'line': 2, 'column': 3}], 'path': ['translation']})


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
