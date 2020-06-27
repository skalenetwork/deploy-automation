#!/usr/bin/env bash

set -e
set -o pipefail

: "${ETH_PRIVATE_KEY?Need to set ETH_PRIVATE_KEY}"
: "${MANAGER_TAG?Need to set MANAGER_TAG}"
: "${ENDPOINT?Need to set ENDPOINT}"

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cp -R $DIR/artifacts/openzeppelin /tmp/openzeppelin
rm -rf $DIR/artifacts/openzeppelin
mkdir $DIR/artifacts/openzeppelin

# docker pull skalenetwork/skale-manager:$MANAGER_TAG
docker run \
    -v $DIR/artifacts/contracts_data:/usr/src/manager/data \
    -v $DIR/artifacts/build:/usr/src/manager/build \
    --mount type=volume,dst=/usr/src/manager/.openzeppelin,volume-driver=local,volume-opt=type=none,volume-opt=o=bind,volume-opt=device=$DIR/artifacts/openzeppelin \
    -e GASPRICE=$GASPRICE \
    -e ENDPOINT=$ENDPOINT \
    -e PRODUCTION=$PRODUCTION \
    -e PRIVATE_KEY=$ETH_PRIVATE_KEY \
    skalenetwork/skale-manager:$MANAGER_TAG \
    npx truffle migrate --network unique 2>&1 | tee -a sm-container.log

cp $DIR/artifacts/contracts_data/unique.json $DIR/artifacts/abi.json
