## DEBUGGING START
# zmodload zsh/datetime
# setopt PROMPT_SUBST
# PS4='+$EPOCHREALTIME %N:%i> '

# logfile=$(mktemp zsh_profile.XXXXXXXX)
# echo "Logging to $logfile"
# exec 3>&2 2>$logfile

# setopt XTRACE

export ZSH=/Users/lamdav/.oh-my-zsh

# OMZ: theme selector
ZSH_THEME=""

# OMZ: disable annoying prompt to update
# just let it update and hope it doesn't break :D
DISABLE_UPDATE_PROMPT=true

# OMZ: red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# OMZ: command execution time stamp format
HIST_STAMPS="yyyy-mm-dd"

# OMZ: load OMZ ecosystem
source $ZSH/oh-my-zsh.sh

# ssh
export SSH_KEY_PATH="~/.ssh/rsa_id"

# Aliases
alias editzsh="vim ~/.zshrc"
# This will lose history but it avoid powerline theme prompt issues.
alias refreshzsh="exec zsh"
alias updateplugins="antibody bundle < ~/.zsh_plugins > ~/.zsh_plugins.sh"
# lazy load: jabba
alias loadjabba="source \"/Users/lamdav/.jabba/jabba.sh\""
# lazy load: nvm
export NVM_DIR="$HOME/.nvm"
alias loadnvm="\. \"$HOME/.nvm/nvm.sh\""
# lazy load: pyenv (called by powerlevel10k `pyenv`)
# alias loadpyenv="eval \"$(pyenv init -)\""

# antibody + powerline theme
source ~/.zsh_plugins.sh
source ~/.purepower

# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin:/Users/lamdav/Library/Python/3.7/bin:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
export PATH="$PATH:$HOME/anaconda3/bin"

export TERM=xterm-256color

# heroku autocomplete setup
HEROKU_AC_ZSH_SETUP_PATH=/Users/lamdav/Library/Caches/heroku/autocomplete/zsh_setup && test -f $HEROKU_AC_ZSH_SETUP_PATH && source $HEROKU_AC_ZSH_SETUP_PATH;

## DEBUGGING END
# unsetopt XTRACE
# exec 2>&3 3>&-
