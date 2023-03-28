#!/bin/sh

cd $(dirname $0)/..

pip install -r requirements.txt
pip install -r requirements_dev.txt
pre-commit install
