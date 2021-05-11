#!/bin/bash
###############################################################################
# Recreates a venv tailored to this project.
# 
# Used environment variables:                               | Defaults to:    |
# VENV_PATH:   # The path where to create the venv.         | ./venv          |
# PYTHON:      # The python executable to create venv with. | $(deactivate \  |
#                                                           | && which python)|
#
###############################################################################

set -eu
if [[ $PWD != */jeroenbos.partest ]]; then
    echo "fatal: Invoke from root directory"
    exit 1
fi

VENV_PATH=${VENV_PATH:-"./venv"}
VENV_PATH=$(realpath "$VENV_PATH")

ON_WINDOWS=0 && [[ "$(uname -s)" =~ ^MINGW ]] && ON_WINDOWS=1
# On Windows, the activate script is in the directory "$VENV_PATH/Scripts".
# On Unix it's "$VENV_PATH/bin"
if [ "$ON_WINDOWS" ]; then 
    VENV_ACTIVATE_PATH="$VENV_PATH/Scripts/activate"
else
    VENV_ACTIVATE_PATH="$VENV_PATH/bin/activate"
fi


if [ -d "$VENV_PATH" ] ; then
    echo Deleting previous venv...
    if [ -f "$VENV_ACTIVATE_PATH" ]; then
        "$VENV_ACTIVATE_PATH" deactivate
    fi 
    # A move is a near-instantaneous operation
    mv "$VENV_PATH" "./.old-venv"
    # Slow removal is in the background
    rm -r "./.old-venv" &
fi

# Finding python must happen after deactivation of the previous venv
PYTHON=${PYTHON:-$(which python)}

echo Creating venv...
"$PYTHON" -m venv "$VENV_PATH"

if [ "$ON_WINDOWS" ]; then
    # Workaround for bug in the activate script:
    # On windows VIRTUAL_ENV will be set using windows path separators,
    # but later the script combines it with unix path separators.
    # We just replace setting VIRTUAL_ENV before we call activate.
    # An invalid path would otherwise crop into $PATH and then we'd be a long way from home.

    sed -i "s~VIRTUAL_ENV=.*~VIRTUAL_ENV=\"$VENV_PATH\"~g" "$VENV_ACTIVATE_PATH"
fi

echo Sourcing venv...
source "$VENV_ACTIVATE_PATH"

echo Installing packages...
python -m pip install --upgrade pip

# Performance optimization for package installation:
pip install wheel  

# Install development-only packages:
pip install -r requirements.dev.txt

pip install -r requirements.txt
