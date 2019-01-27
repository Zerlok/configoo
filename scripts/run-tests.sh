#!/bin/bash

PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) )

PYTHONPATH=$PROJECT_DIR/src pytest -p no:cacheprovider $PROJECT_DIR/test
