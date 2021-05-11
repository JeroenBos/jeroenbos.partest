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
    exit 1
fi

if [ "$#" -gt 0 ]; then
    if [ "$1" = "--clean" ]; then
        source ./scripts/venv.sh
    else
        echo Unrecognized argument "$1"
        exit 1
    fi
fi

echo Building...
python -m build

echo "removing ./src/*.egg-info/"
rm -r ./src/*.egg-info/
echo "removing ./build/"
rm -r ./build/

echo Done 
