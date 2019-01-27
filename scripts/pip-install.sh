#!/bin/bash

packages=( ${*} )

pip install ${packages[*]} || exit 1

if [[ -f ./requirements.txt ]]; then
    locked_packages=( $( cat ./requirements.txt | awk -F '==' '{ print $1 }' ) )
else
    locked_packages=()
fi

pattern=$(
    python -c "\
packages = set('${packages[*]}'.split(' '))
packages.update('${locked_packages[*]}'.split(' '))
print('|'.join(packages))
    "
)

pip freeze | grep -E $pattern > requirements.txt
