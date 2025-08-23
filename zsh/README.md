# Modular Zsh Configuration

This directory contains a modular Zsh configuration that splits the traditional monolithic `.zshrc` into focused, maintainable modules.

## 📁 Module Structure

### Core Modules (loaded in order)

1. **`options.zsh`** - ZSH options and behavior configuration
   - History settings (50k lines, deduplication)
   - Directory navigation (auto_cd, pushd behavior)
   - Completion behavior (auto_menu, smart completion)
   - Globbing and expansion (extended_glob, case insensitive)
   - Safety features (spell correction, no_clobber)

2. **`completion.zsh`** - Completion system setup
   - Optimized compinit (daily regeneration)
   - Completion styling and colors
   - Process and user filtering
   - Caching for performance

3. **`keybindings.zsh`** - Key bindings configuration
   - Emacs-style key bindings (configurable)
   - Enhanced history search (up/down arrow)
   - Terminal application mode support
   - Word movement and deletion
   - Command line editing

4. **`environment.zsh`** - Environment variables and PATH
   - Core environment (EDITOR, PAGER, etc.)
   - Language/locale settings
   - Tool-specific configurations
   - Optimized PATH construction
   - External integrations (Google Cloud SDK)

5. **`lazy-loading.zsh`** - Performance-optimized lazy loading
   - Generic lazy loading functions
   - Node.js (NVM) with smart binary detection
   - Python (pyenv) integration
   - Java (JABBA) support
   - Prevents startup slowdown

6. **`aliases.zsh`** - Aliases and utility functions
   - Modern CLI tool replacements (eza, bat, rg)
   - Git workflow aliases
   - Safety aliases (rm -i, cp -i, mv -i)
   - Utility functions (mkcd, extract, benchmarkzsh)
   - Alias listing command

7. **`integrations.zsh`** - External tool integrations
   - Claude Code integration
   - Kitty terminal enhancements
   - Antidote plugin manager
   - Powerlevel10k configuration
   - Custom configuration support

## 🚀 Benefits

### Performance
- **Faster startup**: Lazy loading prevents blocking operations
- **Optimized completion**: Daily compinit regeneration
- **Efficient PATH**: Single construction without duplicates
- **Smart caching**: Plugin and completion caching

### Maintainability
- **Focused modules**: Each file has a single responsibility
- **Easy debugging**: Enable profiling with `zmodload zsh/zprof`
- **Version control**: Track changes to specific functionality
- **Documentation**: Each module is self-documenting

### Flexibility
- **Selective loading**: Skip modules by commenting out
- **Easy customization**: Modify individual modules
- **Fallback support**: Graceful handling of missing files
- **Custom extensions**: Add your own modules

## 🔧 Usage

### Main Commands

```bash
# List all available aliases
aliases

# Benchmark shell performance
benchmarkzsh

# Update plugins
updateplugins

# Edit main configuration
editzsh

# Reload configuration
refreshzsh
```

### Kitty Integration (when using Kitty terminal)

```bash
# Show kitty shortcuts
kitty-help

# Session management
ksave <name>    # Save current session
kload <name>    # Load saved session

# Smart splitting
ksplit          # Intelligent split based on window size

# Notifications
knotify <cmd>   # Monitor command and notify on completion

# Theme switching
ktheme          # Switch theme based on directory
```

### Development Tools (lazy-loaded)

```bash
# Node.js
nvm use <version>
npm install
node script.js

# Python
pyenv global <version>
python script.py

# Java
loadjabba
jabba use <version>
```

## 🛠 Customization

### Adding New Modules

1. Create new `.zsh` file in this directory
2. Add module name to `zsh_modules` array in `~/.zshrc`
3. Follow the existing module structure with clear sections

### Custom Configuration

Create `~/.zshrc_custom` for personal customizations that won't be tracked in version control.

### Environment-Specific Settings

Modules automatically adapt to available tools:
- Only loads integrations if tools are installed
- Graceful fallbacks for missing dependencies
- Conditional feature enablement

## 🐛 Troubleshooting

### Performance Issues
```bash
# Enable profiling
# Uncomment first line in ~/.zshrc: zmodload zsh/zprof
refreshzsh
# Check output at bottom of shell startup

# Benchmark startup time
benchmarkzsh
```

### Module Loading Issues
```bash
# Check for error messages during startup
# Modules with issues will show warning messages

# Verify module files exist
ls -la ~/.config/zsh/

# Test individual modules
source ~/.config/zsh/options.zsh
```

### Missing Features
```bash
# Check if tools are installed
which eza bat rg fd

# Install missing tools
brew install eza bat ripgrep fd-find

# Reload to enable new features
refreshzsh
```

## 📋 Module Dependencies

- **options.zsh**: No dependencies
- **completion.zsh**: Requires `options.zsh`
- **keybindings.zsh**: Requires `completion.zsh`
- **environment.zsh**: No dependencies
- **lazy-loading.zsh**: Requires `environment.zsh`
- **aliases.zsh**: Requires all previous modules
- **integrations.zsh**: Requires all previous modules

Loading order is important and handled automatically by the main `.zshrc` file.