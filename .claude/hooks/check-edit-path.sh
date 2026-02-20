#!/usr/bin/env bash
# PreToolUse hook: warn when editing files outside the dotfiles directory.
# Prevents the classic "edited the symlink target instead of the source" mistake.

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

dotfiles_dir="$HOME/configs/dotfiles"
real_path=$(realpath "$file_path" 2>/dev/null || echo "$file_path")

if [[ "$real_path" != "$dotfiles_dir"* ]]; then
  echo "WARNING: Editing outside dotfiles directory: $file_path" >&2
  echo "Ensure you are editing the source file, not a symlink target." >&2
fi

exit 0  # warn only, do not block
