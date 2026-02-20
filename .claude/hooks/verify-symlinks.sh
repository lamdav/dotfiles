#!/usr/bin/env bash
# PostToolUse hook: run symlink status check after installer files are edited.
# Catches broken symlinks immediately instead of at next install run.

input=$(cat)
file_path=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null)

[[ -z "$file_path" ]] && exit 0

if [[ "$file_path" == *"symlink_manager"* ]] || [[ "$file_path" == *"dotfiles_installer"* ]]; then
  echo "--- Installer file changed: running symlink status check ---" >&2
  cd "$HOME/configs/dotfiles" && python3 installer/main.py status
fi

exit 0
