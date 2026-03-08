# macOS-specific Completion Configuration

# Google Cloud SDK completion (Homebrew path)
if [[ -f "/opt/homebrew/share/google-cloud-sdk/completion.zsh.inc" ]]; then
  source "/opt/homebrew/share/google-cloud-sdk/completion.zsh.inc"
fi

# Explicitly register completions for Homebrew-installed tools
completion_tools=(bat eza rg fd)
for tool in "${completion_tools[@]}"; do
  if command -v "$tool" >/dev/null 2>&1; then
    autoload -U "_$tool" 2>/dev/null && compdef "_$tool" "$tool"
  fi
done
unset completion_tools tool
