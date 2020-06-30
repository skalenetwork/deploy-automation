#!/usr/bin/env bash

set -e
set -o pipefail

: "${ETH_PRIVATE_KEY?Need to set ETH_PRIVATE_KEY}"
: "${MANAGER_TAG?Need to set MANAGER_TAG}"
: "${ENDPOINT?Need to set ENDPOINT}"

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker pull skalenetwork/skale-manager:$MANAGER_TAG
docker run \
    -v $DIR/artifacts/contracts_data:/usr/src/manager/data \
    -v $DIR/artifacts/build:/usr/src/manager/build \
    -v $DIR/artifacts/openzeppelin:/usr/src/manager/.openzeppelin \
    -e GASPRICE=$GASPRICE \
    -e ENDPOINT=$ENDPOINT \
    -e PRODUCTION=$PRODUCTION \
    -e NETWORK=$NETWORK \
    -e PRIVATE_KEY=$ETH_PRIVATE_KEY \
    skalenetwork/skale-manager:$MANAGER_TAG \
    /usr/src/manager/scripts/upgrade.sh 2>&1 | tee -a sm-container.log

cp -R $DIR/artifacts $DIR/upgrade-artifacts-$(date +%Y%m%d%H%M%S)