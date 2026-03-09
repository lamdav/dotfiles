#!/bin/bash
# sync-simplebar-displays.sh
#
# Detects connected monitors and updates simple-bar's customAeroSpaceDisplayIndexes
# so each bar shows the correct workspaces for its physical display.
#
# Übersicht uses CGDirectDisplayIDs for widget URL paths, while AeroSpace reports
# monitor-appkit-nsscreen-screens-id (1-based NSScreen array index). This script
# builds the NSScreenId → CGDisplayId mapping at runtime using the same AppKit
# API that Übersicht uses internally.
#
# Runs automatically via AeroSpace after-startup-command.
# Re-run manually after connecting/disconnecting monitors:
#   ~/.config/ubersicht/simple-bar/sync-simplebar-displays.sh

set -euo pipefail

SIMPLEBARRC="${HOME}/.simplebarrc"

# Build NSScreenId → (adjusted) CGDirectDisplayId mapping via Swift.
# NSScreen.screens is 0-indexed; AeroSpace uses 1-based NSScreen IDs.
#
# simple-bar-context.jsx applies `ubersichtDisplayId - 1` when no built-in
# retina display is present (isAeroSpace && !hasBuiltInRetina). We pre-subtract
# 1 from each CGDisplayId here to compensate, so the values match what
# simple-bar uses after its own adjustment.
MAPPING_JSON=$(swift - 2>/dev/null <<'SWIFT'
import AppKit
let hasBuiltInRetina = NSScreen.screens.contains { $0.localizedName == "Built-in Retina Display" }
var pairs: [String] = []
for (i, screen) in NSScreen.screens.enumerated() {
    if let cgId = screen.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? UInt32 {
        let mappedId = hasBuiltInRetina ? Int(cgId) : Int(cgId) - 1
        pairs.append("\"\(i + 1)\": \(mappedId)")
    }
}
print("{\(pairs.joined(separator: ", "))}")
SWIFT
)

if [[ -z "$MAPPING_JSON" || "$MAPPING_JSON" == "{}" ]]; then
    echo "sync-simplebar-displays: no displays detected, skipping" >&2
    exit 0
fi

# Update simplebarrc using jq. Write via cat to preserve the symlink.
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT
jq --argjson m "$MAPPING_JSON" \
    '.spacesDisplay.customAeroSpaceDisplayIndexes = $m' \
    "$SIMPLEBARRC" > "$TMP"
cat "$TMP" > "$SIMPLEBARRC"

echo "sync-simplebar-displays: updated mapping → $MAPPING_JSON"

# Reload simple-bar to pick up new settings (reload re-executes full JS module
# including Settings.init(); refresh only reruns the shell command + render)
osascript -e 'tell application id "tracesOf.Uebersicht" to reload widget id "simple-bar-index-jsx"' 2>/dev/null || true
