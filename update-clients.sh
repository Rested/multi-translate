#!/usr/bin/env bash

version=$(<VERSION)
# python
docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g python -o /local/clients/python --package-name multitranslateclient \
--git-user-id rekon-oss --git-repo-id multi-translate \
--additional-properties=packageVersion=$version,packageUrl=https://github.com/rekon-oss/multi-translate/clients/python

docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g go -o /local/clients/go --package-name multitranslateclient \
--git-user-id rekon-oss --git-repo-id multi-translate/clients/go \
--additional-properties=packageVersion=$version

docker run --net="host" --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
-i http://localhost:8080/openapi.json -g javascript -o /local/clients/js --package-name multitranslateclient \
--git-user-id rekon-oss --git-repo-id multi-translate \
--additional-properties=npmRepository=https://npm.pkg.github.com/,projectName=@rekon-oss/multi-translate