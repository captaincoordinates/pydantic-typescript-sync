#!/bin/sh

set -e

pre-commit install
pre-commit run --all-files flake8
pre-commit run --all-files mypy
