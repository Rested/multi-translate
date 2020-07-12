# Multi-Translate

<p align="center">
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/rekon-oss/multi-translate/Python unit tests">
    <img alt="GitHub tag (latest by date)" src="https://img.shields.io/github/v/tag/rekon-oss/multi-translate">
    <img alt="License - MIT" src="https://img.shields.io/badge/license-MIT-informational">
</p>

## What is it?

Multi-translate is a unified interface on top of various translate APIs providing optimal translations :star:, 
persistence :floppy_disk:, fallback :recycle:.

Multi-Translate uses `FastApi` and `asyncpg` to keep things snappy :zap:, and offers `graphql` and `json` endpoints.

You can check out a public demo here:

https://multi-translate-public-api.rekon.uk/docs

(redoc)
https://multi-translate-public-api.rekon.uk/redoc

(graphql)
https://multi-translate-public-api.rekon.uk/gql

## Features

#### Optimal Translations :star:

Multi-translate aims to provide optimal translations for the given language pair. It does this by combining the
strengths of the `Amazon`, `Deep L`, `Google`, `Microsoft`, `Naver Papago`, and `Yandex` translation APIs.

User's can specify which engine they want to use with the `preferred_engine` parameter. However there is also the 
default value of `best` for this field.

When `best` is used, the first suitable engines will be filtered out based on required capabilities - for instance if 
`from_language` is not specified and detection is required then engines which do not support detection will be eliminated.
Similarly when `with_alignment` is set to `true` engines which don't support alignment will be eliminated. Finally, if
the language pair is not supported for an engine it will be eliminated. 

The controller will use then [language_preferences.yaml](language_preferences.yaml) (which is configurable) to look up 
the best translation engine for the from/to language combination based on the remaining languages. The default 
preferences are listed in [default_preferred.md](default_preferred.md).

#### Persistence :floppy_disk:

When a result is fetched for a particular engine, language, feature, and source text, it will be stored in a 
`postgres` database, if it has been fetched before, it will be retrieved from the database instead to avoid unnecessary
usage charges. The write to the database takes place after the response is returned to keep responses fast :zap:.

#### Fallback :recycle:

The `fallback` option can be used so that if a result fails for the specified engine, for whatever reason, then the next
best valid engine in the list will be chosen.


#### Rate limiting

Rate limiting is optionally built in.



## Installation

### Helm Chart

The helm chart is the easiest way to install

```bash
helm repo add rekon http://charts.rekon.uk
helm repo update
helm upgrade --install multi-translate rekon/multi-translate
``` 

Documentation for values can be found in [charts/multi-translate/README.md](charts/multi-translate/README.md)

### Docker image

You can download the docker image with:
```bash
docker pull rekonuk/multi-translate
```

To determine which env variables to set you can look at [settings.py](settings.py) and 
[charts/multi-translate/README.md](charts/multi-translate/README.md).


## Access

### JSON API

The core `translate` endpoint can be found at `GET /translate` or `POST /translate`. Documentation is available in `swagger` and `redoc` 
style at `/docs` and `/redoc` respectively.

#### Example (python)

```python
import httpx
request_data = {
    "to_language": "es",
    "source_text": "How do you do?",
    "with_alignment": True,
}
resp = httpx.get("http://localhost:8080/translate", params=request_data)
post_resp = httpx.post("http://localhost:8080/translate", json=request_data)

assert resp.status_code == post_resp.status_code == 200
result = resp.json()
post_result = post_resp.json()

assert result == post_result == {
    "translated_text": "¿Cómo estás?",
    "engine": "microsoft",
    "engine_version": "3.0",
    "from_language": "en",
    "to_language": "es",
    "source_text": "hello",
    "detected_language_confidence": "1.0",
    "alignment": [
        {
            "dest": {"end": "4", "start": "0", "text": "안녕하세요"},
            "src": {"end": "4", "start": "0", "text": "hello"},
        }
    ],
}
```

### Graphql

The graphql endpoint is available (with `GraphiQL` UI) at `/gql`

#### Example (gql)

```graphql
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
```

Result 

```json
{
  "data": {
    "translation": {
      "translatedText": "¿Cómo estás?",
      "fromLanguage": "en",
      "alignment": [
        {
          "src": {
            "start": 0,
            "end": 13,
            "text": "How do you do?"
          },
          "dest": {
            "start": 0,
            "end": 11,
            "text": "¿Cómo estás?"
          }
        }
      ]
    }
  }
}
```

### Clients

Autogenerated OpenAPI 3.0 clients are available for `go`, `python` and `javascript`.

You can see examples and installation instructions [here](clients/README.md#Examples).


## Development

Run the app using skaffold
```bash
skaffold dev --port-forward
```

Run the functional tests once the app is running and port-forwarded
```bash
pytest functional_tests/ -vv
```

## Documentation

The helm chart documentation is autogenerated with `helm-docs`
```bash
docker run --rm -v "$(pwd):/helm-docs" -u $(id -u) jnorwood/helm-docs:latest
```

The api documentation is contained within the API Clients and will be hosted on your instance at `/docs` and `/redoc`.