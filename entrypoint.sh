#!/bin/bash

find "${INPUT_BASE_DIR}" -type f -name requirements.txt -exec echo "Installing requirements found at {}" \; -exec pip install -r {} \;

export PYTHONPATH=$PYTHONPATH:$INPUT_BASE_DIR
echo "PYTHONPATH: $PYTHONPATH"

"$@"
