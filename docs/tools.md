# Tool Reference

Quick reference for every major tool in this setup.

---

## Shell Navigation

| Command | Description |
|---------|-------------|
| `cd <fuzzy>` | Smart cd via zoxide — learns from history |
| `cdi` | Interactive directory picker (fzf + zoxide) |
| `wd add <name>` | Bookmark current directory |
| `wd <name>` | Jump to bookmarked directory |
| `wd ls` | List all bookmarks |
| `..` / `...` / `....` | Go up 1/2/3 directories |

---

## File Operations

| Command | Tool | Description |
|---------|------|-------------|
| `ls` | eza | Long list with git status |
| `ll` | eza | Full long list |
| `tree` | eza | Tree view |
| `cat <file>` | bat | Syntax-highlighted view |
| `find <pattern>` | fd | Fast file search |
| `grep <pattern>` | ripgrep | Fast content search |

**fd examples:**
```bash
fd -e go              # find all .go files
fd -t d node_modules  # find directories named node_modules
fd --hidden .env      # find hidden files matching .env
```

**rg examples:**
```bash
rg "TODO"             # search current dir recursively
rg -t go "func main"  # search only Go files
rg -l "pattern"       # list matching files only
rg -C 3 "error"       # show 3 lines of context
```

---

## FZF (Fuzzy Finder)

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Fuzzy history search |
| `Ctrl+T` | Fuzzy file picker (inserts path) |
| `Alt+C` | Fuzzy cd into directory |

Inside any fzf prompt: `Ctrl+/` toggles preview pane.

**In Neovim:**
```
<leader>ff  Find files
<leader>fg  Live grep (ripgrep)
<leader>fb  Open buffers
<leader>fr  Recent files
<leader>gc  Git commits
<leader>gb  Git branches
```

---

## Git

```bash
# Daily operations
git s               # status
git co <branch>     # checkout
git ci -m "msg"     # commit
git amend           # amend last commit (no editor)
git undo            # soft reset last commit
git unstage <file>  # unstage a file
git cleanup         # delete merged branches

# Inspection
git l               # oneline log
git graph           # visual graph log
git logp            # compact log with author
git ls-alias        # list all aliases

# Sync
git f               # fetch
git p               # push
git pl              # pull (rebases by default)

# Diff (delta pager)
git diff            # unstaged changes
git show            # last commit
```

**rerere** is enabled — git remembers conflict resolutions and replays them automatically on rebase.

**Work repos:** put them under `~/work/` and `~/.gitconfig-work` is applied automatically (different email).

---

## mise (Version Manager)

Replaces nvm, pyenv, jabba.

```bash
mise ls                        # list active versions
mise install                   # install from config
mise use node@lts              # switch in current project
mise use --global python@3.12  # switch globally
mise upgrade                   # upgrade to latest matching constraint
mise exec -- <cmd>             # run with mise env without activating
mise env                       # show what mise would export
```

**Per-project** (`.mise.toml`):
```toml
[tools]
node = "20"
python = "3.11"
```

Then `use mise` in `.envrc` to auto-activate with direnv.

---

## direnv

Auto-loads `.envrc` when you `cd` into a directory.

```bash
direnv allow        # trust .envrc in current dir
direnv deny         # revoke trust
direnv reload       # reload current .envrc
direnv edit         # open .envrc in $EDITOR
```

**Common `.envrc` patterns:**
```bash
# Python virtualenv
layout python

# Node (adds node_modules/.bin to PATH)
layout node

# Go (project-local GOPATH)
layout go

# mise tools from .mise.toml
use mise

# Simple env vars
export DATABASE_URL="postgres://localhost/myapp"
export API_KEY="$(cat .api_key)"
```

---

## Neovim

Leader key: `<Space>`

### Navigation
```
<leader>ff    Find files (telescope)
<leader>fg    Live grep
<leader>fb    Buffers
<leader>fr    Recent files
<leader>e     File explorer (neo-tree)
<C-h/j/k/l>  Window navigation
<S-h> / <S-l> Previous/next buffer
```

### LSP
```
gd      Definition
gD      Declaration
gr      References
gi      Implementation
K       Hover docs
<leader>rn  Rename
<leader>ca  Code action
<leader>cf  Format
<leader>d   Diagnostics float
[d / ]d     Prev/next diagnostic
```

### Git (gitsigns)
```
]h / [h       Next/prev hunk
<leader>hs    Stage hunk
<leader>hr    Reset hunk
<leader>hp    Preview hunk
<leader>hb    Blame line
<leader>hd    Diff this
```

### Plugin management
```
:Lazy          Open plugin manager
:Lazy sync     Update all plugins
:Mason         Open LSP server manager
:LspInfo       Show active LSP servers
:TSUpdate      Update treesitter parsers
```

---

## GitHub CLI (gh)

```bash
gh auth login           # authenticate
gh repo clone <repo>    # clone a repo
gh pr create            # create pull request (interactive)
gh pr list              # list open PRs
gh pr checkout <num>    # checkout a PR locally
gh pr review <num>      # review a PR
gh issue create         # create issue
gh issue list           # list issues
gh run list             # list CI runs
gh run view <id>        # view CI run details
gh run watch            # watch live CI run
```

---

## btop

Replaces `top`. Launch with `top` (aliased).

Key bindings inside btop:
- `q` — quit
- `m` — toggle memory layout
- `p` — toggle process view
- `k` — kill selected process
- `F2` — settings
- Arrow keys — navigate

---

## Kitty Terminal

```
cmd+t           New tab
cmd+w           Close pane (tab if last pane)
cmd+d           Split horizontal
cmd+shift+d     Split vertical
cmd+1-9         Jump to tab N
cmd+0           Jump to last tab
cmd+k           Clear + scrollback
cmd+shift+z     Toggle pane fullscreen
cmd++ / cmd+-   Font size up/down
ctrl+`          Toggle hotkey window (Quake-style)
```

`kitty-help` — print all keybindings from config.

---

## AeroSpace

All bindings use `alt+`:

```
alt+h/j/k/l         Focus window left/down/up/right
alt+shift+h/j/k/l   Move window
alt+1-9             Switch workspace
alt+shift+1-9       Move window to workspace
alt+s/f/m           Switch to Spotify/Finder/Mail workspace
alt+tab             Back-and-forth workspace
alt+shift+;         Service mode (layout ops)
alt+shift+r         Resize mode (then h/j/k/l)
alt+shift+'         Media mode (Spotify controls)
```
