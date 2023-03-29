#!/bin/bash

if [[ -z "${REQUIREMENTS_FILES}" ]]; then
    echo "no requirements files to install"
else
    if [ "${REQUIREMENTS_FILES}" == "discover" ]; then
        find "${INPUT_BASE_DIR}" -type f -name requirements.txt -exec echo "installing {}" \; -exec pip install -r {} \;
    else
        echo "${REQUIREMENTS_FILES}" | jq -r -c '.[]' | while read REQ_FILE; do
            echo "installing ${REQ_FILE}"
            pip install -r "${REQ_FILE}"
        done
    fi
fi

export PYTHONPATH=$PYTHONPATH:$INPUT_BASE_DIR
echo "PYTHONPATH: $PYTHONPATH"

"$@"
