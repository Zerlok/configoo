#!/bin/bash

[[ -z $( which pip ) ]] && \
    echo "Pip is not installed, exiting ..." && \
    exit 1

PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) ) || exit 1
REQUIREMENTS_FILE=$PROJECT_DIR/requirements.txt

PARSED_ARGS=$( python -c"\
args = '${*}'.split(' ')

options_index = args.index('--') if '--' in args else len(args)
options = args[options_index + 1:]

installing_packages = set(args[:options_index])
installed_packages = set(line['name'] for line in $( pip list --format json ))
required_to_install_packages = installing_packages - installed_packages

print('|'.join((
    ' '.join(required_to_install_packages),
    ' '.join(options)
)))
" ) || exit 1

PACKAGES=( $( echo ${PARSED_ARGS[@]} | awk -F'|' '{ print $1 }' ) )
OPTIONS=( $( echo ${PARSED_ARGS[@]} | awk -F'|' '{ print $2 }' ) )

[[ -z "${PACKAGES[@]}" ]] && \
    echo "Nothing to install, exiting ..." && \
    exit 0


echo "Installing ${PACKAGES[@]} packages ..."
pip install ${OPTIONS[*]} ${PACKAGES[*]}
status=$?
if [[ $status != 0 ]]; then
    echo "Failed to install packages, exiting ..."
    exit $status
fi


echo "Locking packages in requirements file ..."

python -c "\
locking_packages = set('${PACKAGES[*]}'.split(' '))

with open('${REQUIREMENTS_FILE}', 'a') as fd:
    for line in $( pip list --format json ):
        if line['name'] in locking_packages:
            fd.write(f'''{line['name']}~={line['version']}\n''')
" && \
    echo "Done." && \
    exit 0
