#!/usr/bin/env bash

docker run --rm -v "$(pwd):/helm-docs" -u $(id -u) jnorwood/helm-docs:latest
