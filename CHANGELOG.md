## [1.0.1] - 2026-03-15

### 🚜 Refactor

- Replace hardcoded phase numbers with dynamic counter in Ubuntu installer
## [1.0.0] - 2026-03-15

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
- Add git-cliff versioning and release workflow
