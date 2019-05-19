export ZSH=/Users/lamdav/.oh-my-zsh

# OMZ: theme selector
ZSH_THEME=""

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

# antibody + powerline theme
source ~/.zsh_plugins.sh
source ~/.purepower

# jabba
[ -s "/Users/lamdav/.jabba/jabba.sh" ] && source "/Users/lamdav/.jabba/jabba.sh"

# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin:/Users/lamdav/Library/Python/3.7/bin:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
export PATH="$PATH:$HOME/anaconda3/bin"



# heroku autocomplete setup
HEROKU_AC_ZSH_SETUP_PATH=/Users/lamdav/Library/Caches/heroku/autocomplete/zsh_setup && test -f $HEROKU_AC_ZSH_SETUP_PATH && source $HEROKU_AC_ZSH_SETUP_PATH;function gi() { curl -sLw n https://www.gitignore.io/api/$@ ;}

# pyenv
eval "$(pyenv init -)"
