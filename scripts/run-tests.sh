#!/bin/bash

PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) )

SRC_DIR=$PROJECT_DIR/src
TEST_DIR=$PROJECT_DIR/test

export PYTHONPATH=$SRC_DIR

path=${1:-"${TEST_DIR}"}

if [[ -z $1 ]]; then
    cov=" \
        --cov-config $TEST_DIR/.coveragerc \
        --cov $SRC_DIR \
    "
fi

pytest \
    -p no:cacheprovider \
    $cov \
    $path

[[ -n $cov ]] && \
    rm -f $PWD/.coverage
