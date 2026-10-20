## [1.3.0] - 2026-10-20

### 🚀 Features

- Add batmd function for glow+bat markdown viewing
- Expand brew toolset and add cloud/database Brewfiles
- Add glow markdown viewer to devtools
- Auto-trust third-party brew taps before bundling
- Add simple-bar widget updates to maintenance routine
- Add glow config with dark style, pager, and TUI defaults
- Track Claude Code and Gemini CLI conductor configs
- Symlink Claude Code settings via installer
- Add atuin for history search and dust for disk usage
- Swap ranger for yazi file manager
- Migrate pre-commit, poetry, commitizen from pipx to mise pypi backend
- Add xh and jaq as faster httpie/jq alternatives
- Track atuin config in dotfiles, enable daemon mode, add Dracula theme
- Fix Dracula theme structure, add vim keymap and richer columns to atuin
- Track d2 in Brewfile.devtools
- Migrate golangci-lint and gradle from brew to mise
- Add envrc-init for one-command .envrc scaffolding

### 🐛 Bug Fixes

- Disable glow pager to stop raw ANSI codes leaking to output
- Revert atuin to default theme, dracula.toml was incomplete
- Bump transitive virtualenv 21.3.1 -> 21.14.5 (security)

### ⚙️ Miscellaneous Tasks

- Swap gemini-cli for antigravity-cli, drop chromedriver
- Update nvim plugin lockfile
- Sync Claude Code settings, drop stray autoMode trust block
- Release v1.3.0
- Drop httpie, jq, and tree — fully shadowed by their replacements
- Drop duplicate go and broken yarn from brew, use mise+corepack
- Remove unused Brewfile.databases, fix stale jq/httpie doc mention
- Remove unused bash-completion (zsh uses native compinit, not bashcompinit)
## [1.2.0] - 2026-03-15

### 🚀 Features

- Extend layout uv with --pyproject=<subdir> flag

### ⚙️ Miscellaneous Tasks

- Update .envrc layout command to dot
- Release v1.2.0
## [1.1.1] - 2026-03-15

### ⚙️ Miscellaneous Tasks

- Add uv.lock for reproducible installs
- Release v1.1.1
## [1.1.0] - 2026-03-15

### 🚀 Features

- Implement dot CLI with release workflow

### 🐛 Bug Fixes

- Show help when dot is invoked with no arguments

### ⚙️ Miscellaneous Tasks

- Remove bin/release in favor of upcoming dot CLI
- Release v1.1.0
## [1.0.1] - 2026-03-15

### 🚀 Features

- Add Kitty quick-access-terminal setup for Quake-style dropdown
- Add mise, neovim, direnv, fzf, and zoxide integration
- Add trouble.nvim, todo-comments.nvim, and oil.nvim
- Add workspace-to-monitor assignments and new workspaces T/Y
- Add sync scope to maintain skill for interactive install health check
- Add borders config file and symlink
- Switch kitty tab bar from custom script to native fade style
- Update borders to bold cyan glow, width 8
- Support dual-monitor home setup in workspace assignments
- Include ~/.config/git/.gitconfig-local for machine-local git overrides
- Add Ubuntu server support with cross-platform zsh layer architecture
- Add gh, git-delta, btop, httpie, ncdu to Ubuntu installer
- Add uv to macOS and Ubuntu installs, add layout uv to direnvrc
- Migrate from poetry to uv, add uv zsh completion, drop rm -i alias
- Extend layout uv to generate zsh completions for venv CLI tools

### 🐛 Bug Fixes

- Remove invalid --no-lock flag from brew bundle commands
- Remove deprecated homebrew/bundle tap references
- Check git availability before cloning simple-bar
- Update Kitty key bindings and fix configuration errors
- Clean up shell, git, neovim, and installer gaps
- Make AeroSpace mode tracker paths portable
- Make git config machine-agnostic
- Update installer for machine-agnostic deployment
- Update Brewfiles for portability
- Update kitty tab bar config
- Remove --long flag from ls alias
- Add .zlogin to symlink_manager shell_configs
- Override npm registry in Mason to bypass Uber's internal registry
- Avoid race condition when syncing displays on service mode exit
- Correct git config install strategy
- Add antidote support for Linux and cross-platform plugin paths
- Bootstrap .gitconfig-local as plain file in installer
- Correct delta deb filename and use jq for GitHub release parsing
- Make layout uv completion work correctly in direnv bash context
- Source direnv completion files instead of calling compdef directly

### 🚜 Refactor

- Implement absolute imports and OSType enum for type safety
- Split integrations and completions by OS layer
- Replace hardcoded phase numbers with dynamic counter in Ubuntu installer

### 📚 Documentation

- Update documentation for cross-platform architecture
- Document AeroSpace troubleshooting and portability patterns
- Add borders to CLAUDE.md directory structure and skill checklists
- Update CLAUDE.md for platform layer and installer changes
- Document direnv completion mechanism in CLAUDE.md and memory
- Update CLAUDE.md with pre-commit, platform layer, and kitty notes

### 🎨 Styling

- Apply black 25.1.0 formatting and update poetry.lock
- Remove unused imports and apply formatting
- Apply pre-commit formatting across all files

### ⚙️ Miscellaneous Tasks

- Add Python .gitignore rules and update configurations
- Bump Python dependencies to latest versions
- Add direnv layout for installer venv
- Update lazy-lock.json
- Update lazy-lock.json
- Ignore Claude settings.local.json.bak files
- Gitignore .direnv/ runtime directory
- Add pre-commit config and fix shellcheck warnings
- Sync simplebarrc property ordering from live config
- Remove deprecated homebrew/cask-fonts tap
- Add git-cliff versioning and release workflow
- Release v1.0.1
