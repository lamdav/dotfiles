#!/bin/bash
# sync-and-reload.sh
#
# Wrapper invoked by AeroSpace service mode (esc). Runs display sync
# synchronously so simplebarrc is fully written before AeroSpace
# reloads its config and simple-bar picks up the new mapping.

set -euo pipefail

SCRIPT_DIR="$(dirname "$0")"

# Block until sync completes (Swift compile + jq write + osascript reload)
"$SCRIPT_DIR/sync-simplebar-displays.sh"

# Now safe to reload AeroSpace config
aerospace reload-config
