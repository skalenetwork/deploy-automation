#!/usr/bin/env bash

echo "::set-env name=PROJECT_DIR::$GITHUB_WORKSPACE"
echo PROJECT_DIR: $GITHUB_WORKSPACE

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export BRANCH=${GITHUB_REF##*/}
echo "Branch $BRANCH"

export VERSION=$(python $PROJECT_DIR/allocator_provision/setup.py --version)
export VERSION=$(bash $PROJECT_DIR/helper-scripts/calculate_version.sh)

echo "::set-env name=VERSION::$VERSION"
echo "Version $VERSION"

export OS=`uname -s`-`uname -m`
export EXECUTABLE_NAME=allocator-$VERSION-$OS

echo "::set-env name=BRANCH::$BRANCH"
echo "::set-env name=EXECUTABLE_NAME::$EXECUTABLE_NAME"
