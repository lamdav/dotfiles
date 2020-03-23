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

# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

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
if [ $(date +'%j') != $(/usr/bin/stat -f '%Sm' -t '%j' ${ZDOTDIR:-$HOME}/.zcompdump) ]; then
  compinit
else
  compinit -C
fi

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
NVM_DIR="$HOME/.nvm"

# Skip adding binaries if there is no node version installed yet
if [ -d $NVM_DIR/versions/node ]; then
  NODE_GLOBALS=(`find $NVM_DIR/versions/node -maxdepth 3 \( -type l -o -type f \) -wholename '*/bin/*' | xargs -n1 basename | sort | uniq`)
fi
NODE_GLOBALS+=("nvm")

load_nvm () {
  # Unset placeholder functions
  for cmd in "${NODE_GLOBALS[@]}"; do unset -f ${cmd} &>/dev/null; done

  # Load NVM
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

  # (Optional) Set the version of node to use from ~/.nvmrc if available
  nvm use 2> /dev/null 1>&2 || true

  # Do not reload nvm again
  export NVM_LOADED=1
}

for cmd in "${NODE_GLOBALS[@]}"; do
  # Skip defining the function if the binary is already in the PATH
  if ! which ${cmd} &>/dev/null; then
    eval "${cmd}() { unset -f ${cmd} &>/dev/null; [ -z \${NVM_LOADED+x} ] && load_nvm; ${cmd} \$@; }"
  fi
done

# lazy load: pyenv (called by powerlevel10k `pyenv`)
load_pyenv() {
  eval "$(pyenv init -)"
}

# https://stackoverflow.com/questions/1904860/how-to-remove-unreferenced-blobs-from-my-git-repo
alias git-clean='git -c gc.reflogExpire=0 -c gc.reflogExpireUnreachable=0 -c gc.rerereresolved=0 -c gc.rerereunresolved=0 -c gc.pruneExpire=now gc "$@"'

git-prune() {
    # Delete local branches that squash-merged to `master`. Forked from https://github.com/not-an-aardvark/git-delete-squashed
    git remote prune origin &&
    git checkout -q master &&
    git fetch origin &&
    git fetch --tags -f &&
    git merge --ff-only origin/master &&
    git for-each-ref refs/heads/ "--format=%(refname:short)" | while read branch; do
        mergeBase=$(git merge-base master $branch) &&
        [[ $(
                git cherry master $(
                    git commit-tree $(
                        git rev-parse $branch^{tree}
                    ) -p $mergeBase -m _
                )
            ) == "-"*
        ]] && git branch -D $branch;
    done;
    git prune
}

lazy_load() {
    # Act as a stub to another shell function/command. When first run, it will load the actual function/command then execute it.
    # E.g. This made my zsh load 0.8 seconds faster by loading `nvm` when "nvm", "npm" or "node" is used for the first time
    # $1: space separated list of alias to release after the first load
    # $2: file to source
    # $3: name of the command to run after it's loaded
    # $4+: argv to be passed to $3
    echo "Lazy loading $1 ..."

    # $1.split(' ') using the s flag. In bash, this can be simply ($1) #http://unix.stackexchange.com/questions/28854/list-elements-with-spaces-in-zsh
    # Single line won't work: local names=("${(@s: :)${1}}"). Due to http://stackoverflow.com/questions/14917501/local-arrays-in-zsh   (zsh 5.0.8 (x86_64-apple-darwin15.0))
    local -a names
    if [[ -n "$ZSH_VERSION" ]]; then
        names=("${(@s: :)${1}}")
    else
        names=($1)
    fi
    unalias "${names[@]}"
    . $2
    shift 2
    $*
}

group_lazy_load() {
    local script
    script=$1
    shift 1
    for cmd in "$@"; do
        alias $cmd="lazy_load \"$*\" $script $cmd"
    done
}

export NVM_DIR=~/.nvm
group_lazy_load $HOME/.nvm/nvm.sh node npm

export PATH="$PATH:$HOME/.rvm/bin" # Add RVM to PATH for scripting
group_lazy_load $HOME/.rvm/scripts/rvm rvm irb rake rails

# antibody + powerline theme
source ~/.zsh_plugins.sh

# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="/usr/local/sbin:$PATH"
export PATH="/usr/local/bin:$PATH"
export PATH="$PATH:$HOME/.rvm/bin"
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
export PATH="$PATH:$HOME/anaconda3/bin"
export PATH="$PATH:$HOME/.cargo/bin"
export PATH="$PATH:$HOME/go/bin"
export PATH="$PATH:$HOME/google-cloud-sdk/bin"
export PATH="$PATH:$HOME/.poetry/bin"

export TERM=xterm-256color

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

source ~/.zshrc_custom

## ALTERNATIVE DEBUG TOOL END
# zprof

## DEBUGGING END
# unsetopt XTRACE
# exec 2>&3 3>&-
