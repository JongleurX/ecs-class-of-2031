#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "Error: virtual environment not found at $VENV_PATH"
    exit 1
fi

source "$VENV_PATH/bin/activate"

QT_PLUGINS="$VENV_PATH/lib/python3.14/site-packages/PySide6/Qt/plugins"
export QT_QPA_PLATFORM_PLUGIN_PATH="$QT_PLUGINS"
export QT_PLUGIN_PATH="$QT_PLUGINS"
export DYLD_FRAMEWORK_PATH="$VENV_PATH/lib/python3.14/site-packages/PySide6/Qt/lib"
export DYLD_LIBRARY_PATH="$VENV_PATH/lib/python3.14/site-packages/PySide6/Qt/lib"

cd "$SCRIPT_DIR"
python3 -m labs.driver gui
