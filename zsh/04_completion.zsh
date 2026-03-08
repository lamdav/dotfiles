# ZSH Completion System Configuration

# Load and initialize completion system
zmodload -i zsh/complist
WORDCHARS=''

# Only run compinit once per day for performance (OMZ style)
autoload -Uz compinit
# Regenerate dump only if it's missing or older than 24 hours.
# find -mmin works on both macOS and Linux (unlike BSD stat -f).
if [[ ! -f "${ZDOTDIR:-$HOME}/.zcompdump" ]] || \
   [[ -n "$(find "${ZDOTDIR:-$HOME}/.zcompdump" -mmin +1440 2>/dev/null)" ]]; then
  compinit
else
  compinit -C
fi

# Completion styling
zstyle ':completion:*:*:*:*:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z-_}={A-Za-z_-}' 'r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*' special-dirs true
zstyle ':completion:*' list-colors ''
zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#) ([0-9a-z-]#)*=01;34=0=01'
zstyle ':completion:*:*:*:*:processes' command "ps -u $USERNAME -o pid,user,comm -w -w"
zstyle ':completion:*:cd:*' tag-order local-directories directory-stack path-directories

# Use caching for better performance
zstyle ':completion:*' use-cache yes
export ZSH_CACHE_DIR="${HOME}/.zsh/cache"
[[ -d "${ZSH_CACHE_DIR}" ]] || mkdir -p "${ZSH_CACHE_DIR}"
zstyle ':completion:*' cache-path "$ZSH_CACHE_DIR"

# Don't complete uninteresting users
zstyle ':completion:*:*:*:users' ignored-patterns \
        adm amanda apache at avahi avahi-autoipd beaglidx bin cacti canna \
        clamav daemon dbus distcache dnsmasq dovecot fax ftp games gdm \
        gkrellmd gopher hacluster haldaemon halt hsqldb ident junkbust kdm \
        ldap lp mail mailman mailnull man messagebus  mldonkey mysql nagios \
        named netdump news nfsnobody nobody nscd ntp nut nx obsrun openvpn \
        operator pcap polkitd postfix postgres privoxy pulse pvm quagga radvd \
        rpc rpcuser rpm rtkit scard shutdown squid sshd statd svn sync tftp \
        usbmux uucp vcsa wwwrun xfs '_*'
zstyle '*' single-ignored show

# SSH completion from ~/.ssh/config
zstyle ':completion:*:(ssh|scp|rsync):*' hosts $([ -f "${HOME}/.ssh/config" ] && awk '/^Host / { for (i=2; i<=NF; i++) if ($i !~ /[*?]/) print $i }' "${HOME}/.ssh/config")
zstyle ':completion:*:ssh:*' group-order hosts-domain hosts-host users

# =============================================================================
# EXTERNAL TOOL COMPLETIONS
# =============================================================================

# Register completions for commonly used tools
# Simple, reliable approach that just works

# Plugin completions (functions created in plugins module)
if (( $+functions[_wd] )); then
  compdef _wd wd
fi

# uv — Python package manager
command -v uv >/dev/null 2>&1 && eval "$(uv generate-shell-completion zsh)"

