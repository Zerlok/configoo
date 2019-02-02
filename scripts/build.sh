#!/bin/bash

PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) )
BUILD_DIR=$PROJECT_DIR/build
DIST_DIR=$PROJECT_DIR/dist

# rm -rf $BUILD_DIR && python $PROJECT_DIR/setup.py build
rm -rf $BUILD_DIR $DIST_DIR

python $PROJECT_DIR/setup.py sdist bdist_wheel

rm -rf $BUILD_DIR $PROJECT_DIR/src/*.egg-info
