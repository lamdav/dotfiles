---
name: add-tool
description: Add a new CLI tool to the dotfiles setup. Handles the full workflow — Brewfile entry, shell alias, integration hook, and docs update. Use when the user wants to add a new tool to their dotfiles.
argument-hint: "<brew-name> [alias-target] [integration-command]"
allowed-tools: Bash, Read, Edit, Write
---

Add a new tool to the dotfiles following the established pattern. $ARGUMENTS should contain the brew package name, and optionally the command it replaces and its shell integration command.

Example invocations:
- `/add-tool gping` — adds gping (modern ping replacement)
- `/add-tool dust du` — adds dust, aliasing it over `du`
- `/add-tool starship "eval \"$(starship init zsh)\""` — adds with integration

## Workflow

### 1. Gather info
If $ARGUMENTS is incomplete, ask:
- What is the brew package name?
- Does it replace an existing command? (for alias in `10_aliases.zsh`)
- Does it need shell initialization? e.g. `eval "$(tool init zsh)"` (for `99_integrations.zsh`)
- Which Brewfile does it belong in? (devtools / k8s / gui / apps)

### 2. Add to Brewfile
Add `brew "<name>"` to the appropriate file in `brew/`:
- `Brewfile.devtools` — CLI tools, dev utilities
- `Brewfile.k8s` — Kubernetes/cloud tools
- `Brewfile.gui` — desktop apps and fonts
- `Brewfile.apps` — productivity apps

### 3. Add alias (if it replaces a command)
In `zsh/10_aliases.zsh`, add inside the "Modern CLI tool replacements" section:
```zsh
if command -v <tool> >/dev/null 2>&1; then
  alias <old-command>='<tool>'
fi
```

### 4. Add integration (if it needs shell init)
In `zsh/99_integrations.zsh`, add a new section:
```zsh
# =============================================================================
# <TOOL NAME>
# =============================================================================

if command -v <tool> >/dev/null 2>&1; then
  eval "$(<tool> init zsh)"
fi
```

### 5. Install it
```bash
brew install <name>
```

### 6. Update docs
Add the tool to `docs/tools.md` in the appropriate section, and add it to the tool table in `CLAUDE.md` if it replaces a command.

### 7. Verify
```bash
exec zsh
<tool> --version
```

## Rules
- Always wrap aliases in `command -v` guards
- Always wrap integrations in `command -v` guards
- Use `>|` not `>` if writing to any file in shell scripts (no_clobber is set)
- Integrations go in `99_integrations.zsh`, aliases go in `10_aliases.zsh` — never mix
- After editing any `.zsh` file, remind the user to run `exec zsh`
