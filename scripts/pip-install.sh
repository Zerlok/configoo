#!/bin/bash

PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) )
REQUIREMENTS_FILE=$PROJECT_DIR/requirements.txt

PACKAGES=( ${*} )

pip install ${PACKAGES[*]} || exit 1

if [[ -f $REQUIREMENTS_FILE ]]; then
    LOCKED_PACKAGES=( $( cat $REQUIREMENTS_FILE | awk -F '==' '{ print $1 }' ) )
else
    LOCKED_PACKAGES=()
fi

pattern=$(
    python -c "\
packages = set('${PACKAGES[*]}'.split(' '))
packages.update('${LOCKED_PACKAGES[*]}'.split(' '))
print('|'.join(packages))
    "
)

pip freeze | grep -E $pattern > $REQUIREMENTS_FILE
