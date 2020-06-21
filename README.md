# Multi-Translate

## What is it?

Multi-translate is a unified interface on top of various translate APIs providing optimal translations, persistence, fallback.

### Features

#### Optimal Translations

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

#### Persistence  

When a result is fetched for a particular engine, language, feature, and source text, it will be stored in a 
`postgres` database, if it has been fetched before, it will be retrieved from the database instead to avoid unnecessary
usage charges. 

#### Fallback

The `fallback` option can be used so that if a result fails for the specified engine, for whatever reason, then the next
best valid engine in the list will be chosen.

## Installation

### Helm Chart

```bash
helm repo add rekon http://charts.rekon.uk
helm repo update
helm upgrade --install multi-translate rekon/multi-translate
``` 


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