#!/bin/bash

PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) )
BUILD_DIR=$PROJECT_DIR/build

rm -rf $BUILD_DIR && python $PROJECT_DIR/setup.py build
