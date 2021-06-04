#!/bin/bash
###############################################################################
# Builds the distribution artifacts for this project.
# 
# Takes one optional argument:
# $1: "--clean"    # If specified, virtual env will be recreated.
#
###############################################################################


set -eu
if [[ $PWD != */jeroenbos.partest ]]; then
    echo "fatal: Invoke from root directory"
    return 1
fi

if [ "$#" -gt 0 ]; then
    if [ "$1" = "--clean" ]; then
        source ./scripts/venv.sh
    else
        echo "Unrecognized argument \"$1\""
        return 1
    fi
else
    echo "Sourcing venv..."
    VENV_PATH=$(realpath "${VENV_PATH:-"./venv"}")
    ON_WINDOWS=0 && [[ "$(uname -s)" =~ ^MINGW ]] && ON_WINDOWS=1
    # On Windows, the activate script is in the directory "$VENV_PATH/Scripts".
    # On Unix it's "$VENV_PATH/bin"
    if [ "$ON_WINDOWS" ]; then 
        source "$VENV_PATH/Scripts/activate"
    else
        source "$VENV_PATH/bin/activate"
    fi
fi

echo "Cleaning ./dist/"
rm -rf ./dist/


echo "Building..."
python -m build

echo "Removing temporary build artifacts"
rm -rf ./src/*.egg-info/
rm -rf ./build/

echo "Done"
