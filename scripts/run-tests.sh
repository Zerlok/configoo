#!/bin/bash

PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) )

export PYTHONPATH=$PROJECT_DIR/src

pytest \
    -p no:cacheprovider \
    --cov src \
    $PROJECT_DIR/test

rm $PWD/.coverage
