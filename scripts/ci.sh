#!/bin/sh

set -e

cd $(dirname $0)/..

scripts/init.sh

pre-commit run --all-files flake8
pre-commit run --all-files mypy
