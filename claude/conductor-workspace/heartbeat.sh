#!/bin/bash
# Custom heartbeat — replaces agent-deck's broken heartbeat.sh
# Fixes: jq instead of sed, checks ALL sessions not just one group

SESSION="conductor-main"

# Check if conductor is enabled
ENABLED=$(agent-deck conductor status --json 2>/dev/null | jq -r '.enabled // false')
if [ "$ENABLED" != "true" ]; then
    exit 0
fi

# Only send if the session is idle or waiting
STATUS=$(agent-deck session show "$SESSION" --json 2>/dev/null | jq -r '.status // "unknown"')

if [ "$STATUS" = "idle" ] || [ "$STATUS" = "waiting" ]; then
    agent-deck session send "$SESSION" "Heartbeat: Check ALL sessions (run 'agent-deck list --json'). List any that are waiting or in error, auto-respond where safe, and report what needs my attention." --no-wait -q
fi
