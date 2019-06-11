## DEBUGGING START
# zmodload zsh/datetime
# setopt PROMPT_SUBST
# PS4='+$EPOCHREALTIME %N:%i> '

# logfile=$(mktemp zsh_profile.XXXXXXXX)
# echo "Logging to $logfile"
# exec 3>&2 2>$logfile

# setopt XTRACE

## ALTERNATIVE DEBUG TOOL START
# zmodload zsh/zprof

export ZSH=$HOME/.oh-my-zsh

# OMZ: theme selector
ZSH_THEME=""

# OMZ: disable annoying prompt to update
# just let it update and hope it doesn't break :D
DISABLE_UPDATE_PROMPT=true

# OMZ: red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# OMZ: command execution time stamp format
HIST_STAMPS="yyyy-mm-dd"

# OMZ: check zcoredump once a day
autoload -Uz compinit
typeset -i updated_at=$(date +'%j' -r ~/.zcompdump 2>/dev/null || stat -f '%Sm' -t '%j' ~/.zcompdump 2>/dev/null)
if [ $(date +'%j') != $updated_at ]; then
  compinit -i
else
  compinit -C -i
fi

unset updated_at

# OMZ: load OMZ ecosystem
source $ZSH/oh-my-zsh.sh

# ssh
export SSH_KEY_PATH="~/.ssh/rsa_id"

# Aliases
alias editzsh="vim ~/.zshrc"
# This will lose history but it avoid powerline theme prompt issues.
alias refreshzsh="exec zsh"
benchmarkzsh() {
  for i in $(seq 1 10); do /usr/bin/time zsh -i -c exit; done
}
alias updateplugins="antibody bundle < ~/.zsh_plugins > ~/.zsh_plugins.sh"
# lazy load: jabba
alias loadjabba="source \"/Users/lamdav/.jabba/jabba.sh\""
# lazy load: nvm on call or global installs
export NVM_DIR="$HOME/.nvm"
load_nvm() {
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
}
declare -a NODE_GLOBALS=(`find $NVM_DIR/versions/node -maxdepth 3 -type l -wholename '*/bin/*' | xargs -n1 basename | sort | uniq`)
E_GLOBALS+=("node")
NODE_GLOBALS+=("nvm")
for cmd in "${NODE_GLOBALS[@]}"; do
    eval "${cmd}(){ unset -f ${NODE_GLOBALS}; load_nvm; ${cmd} \$@ }"
done
# lazy load: pyenv (called by powerlevel10k `pyenv`)
# alias loadpyenv="eval \"$(pyenv init -)\""

# antibody + powerline theme
source ~/.zsh_plugins.sh
source ~/.purepower

# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:/usr/local/bin"
export PATH="$PATH:$HOME/.rvm/bin"
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
export PATH="$PATH:$HOME/anaconda3/bin"
export PATH="$PATH:$HOME/.cargo/bin"
export PATH="$PATH:$HOME/go/bin"

export TERM=xterm-256color

# heroku autocomplete setup
HEROKU_AC_ZSH_SETUP_PATH=/Users/lamdav/Library/Caches/heroku/autocomplete/zsh_setup && test -f $HEROKU_AC_ZSH_SETUP_PATH && source $HEROKU_AC_ZSH_SETUP_PATH;

## ALTERNATIVE DEBUG TOOL END
# zprof

## DEBUGGING END
# unsetopt XTRACE
# exec 2>&3 3>&-
