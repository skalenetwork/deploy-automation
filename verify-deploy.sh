#!/usr/bin/env bash

set -e
set -o pipefail

: "${MANAGER_TAG?Need to set MANAGER_TAG}"
: "${OPENZEPPELIN_FOLDER_PATH?Need to set OPENZEPPELIN_FOLDER_PATH}"
#: "${ENDPOINT?Need to set ENDPOINT}"

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker pull skalenetwork/skale-manager:$MANAGER_TAG
docker run \
    -v $OPENZEPPELIN_FOLDER_PATH:/usr/src/manager/.openzeppelin \
    -e ENDPOINT=$ENDPOINT \
    -ti \
    skalenetwork/skale-manager:$MANAGER_TAG \
    npx oz verify 2>&1 | tee -a verify-sm-container.log
