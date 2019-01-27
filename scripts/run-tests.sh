#!/bin/bash

PYTHONPATH=$PWD pytest -p no:cacheprovider $PWD/test
