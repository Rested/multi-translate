from urllib.parse import urljoin

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from functional_tests.ft_settings import FTSettings


base = FTSettings().rest_url


def test_graphql_works():
    transport = RequestsHTTPTransport(
        url=urljoin(base, "gql"), verify=False, retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True,)
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

    result = client.execute(query)

    assert result == {
        "translation": {
            "translatedText": "¿Cómo estás?",
            "fromLanguage": "en",
            "alignment": [
                {
                    "src": {"start": 0, "end": 13, "text": "How do you do?"},
                    "dest": {"start": 0, "end": 11, "text": "¿Cómo estás?"},
                }
            ],
        }
    }
