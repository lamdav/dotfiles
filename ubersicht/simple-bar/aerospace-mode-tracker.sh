#!/usr/bin/env bash

# AeroSpace Mode Tracker for simple-bar
# This script maintains the current AeroSpace mode in a temp file

AEROSPACE_MODE_FILE="/tmp/aerospace-current-mode"

# Function to set mode
set_mode() {
    echo "$1" > "$AEROSPACE_MODE_FILE"
}

# Function to get current mode
get_mode() {
    if [[ -f "$AEROSPACE_MODE_FILE" ]]; then
        cat "$AEROSPACE_MODE_FILE"
    else
        echo "main"
    fi
}

# Handle command line arguments
case "$1" in
    "set")
        set_mode "$2"
        ;;
    "get")
        get_mode
        ;;
    *)
        echo "Usage: $0 {set|get} [mode]"
        echo "Current mode: $(get_mode)"
        ;;
esac