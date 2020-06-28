#!/usr/bin/env bash

autoflake --in-place --remove-all-unused-imports . -r --exclude "*clients/python/**/*.py"
importanize .
black . --exclude clients
