Golang

```bash
docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g go -o /local/clients/go --package-name multi-translate-client \
--git-user-id rekon-oss --git-repo-id multi-translate/clients/go
```

Python
```bash
docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g python -o /local/clients/python --package-name multi_translate_client \
--git-user-id rekon-oss --git-repo-id multi-translate
```

Javascript 
```bash
docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g javascript -o /local/clients/js --package-name multi_translate_client \
--git-user-id rekon-oss --git-repo-id multi-translate
```