#!/bin/bash


# Configuration
ENV_NAME="OLM"
APP="../python/oblivionlevelmanagercli.py"


# Main script

# Initial checks
if [[ "${ENV_NAME}" != "${CONDA_DEFAULT_ENV}" ]]; then
    echo "Error: this script requires the conda environment (i.e. ${ENV_NAME})."
    echo "Abort."
    exit 1
fi

# Generate
echo '## Program arguments'
echo ''

echo '### General use:'
echo ''
echo '```'
python ${APP} -h
echo '```'
echo ''

echo '### `new` command:'
echo ''
echo '```'
python ${APP} new -h
echo '```'
echo ''

echo '### `load` command:'
echo ''
echo '```'
python ${APP} load -h
echo '```'
echo ''

echo '### List of commands:'
echo ''
echo '```'
python ${APP} --run help new tmp
echo '```'
echo ''
