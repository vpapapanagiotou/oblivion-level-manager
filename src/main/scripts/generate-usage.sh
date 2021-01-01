#!/bin/bash


# Configuration
ENV_NAME="OLM"
APP="../python/oblivionlevelmanagercli.py"


# Main script

# Initial checks
if [[ "${ENV_NAME}" != "${CONDA_DEFAULT_ENV}" ]]; then
    SHOULD_CHANGE_ENV=1
else
    SHOULD_CHANGE_ENV=0
fi

# Change conda environment if required
if [[ ${SHOULD_CHANGE_ENV} = 1 ]]; then
    conda activate ${ENV_NAME}
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

# Revert back to previous conda environment if required
if [[ ${SHOULD_CHANGE_ENV} = 1 ]]; then
    conda deactivate
fi
