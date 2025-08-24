# Lazy Loading Functions for Better Performance

# Generic lazy loading function
lazy_load() {
    # Act as a stub to another shell function/command. When first run, it will load the actual function/command then execute it.
    # $1: space separated list of alias to release after the first load
    # $2: file to source
    # $3: name of the command to run after it's loaded
    # $4+: argv to be passed to $3
    echo "Lazy loading $1 ..."

    # Split $1 into array (zsh compatible)
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

# Group lazy loading for better performance
group_lazy_load() {
    local script
    script=$1
    shift 1
    for cmd in "$@"; do
        alias $cmd="lazy_load \"$*\" $script $cmd"
    done
}

# Node.js (NVM) lazy loading with optimization
export NVM_DIR="${HOME}/.nvm"

# Skip adding binaries if there is no node version installed yet
if [ -d $NVM_DIR/versions/node ]; then
  NODE_GLOBALS=(`find $NVM_DIR/versions/node -maxdepth 3 \( -type l -o -type f \) -wholename '*/bin/*' | xargs -n1 basename | sort | uniq`)
fi
NODE_GLOBALS+=("nvm")

load_nvm() {
  # Unset placeholder functions
  for cmd in "${NODE_GLOBALS[@]}"; do unset -f ${cmd} &>/dev/null; done

  # Load NVM
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

  # Set the version of node to use from ~/.nvmrc if available
  nvm use 2> /dev/null 1>&2 || true

  # Do not reload nvm again
  export NVM_LOADED=1
}

# Create placeholder functions for node globals
for cmd in "${NODE_GLOBALS[@]}"; do
  # Skip defining the function if the binary is already in the PATH
  if ! which ${cmd} &>/dev/null; then
    eval "${cmd}() { unset -f ${cmd} &>/dev/null; [ -z \${NVM_LOADED+x} ] && load_nvm; ${cmd} \$@; }"
  fi
done

# Alternative group lazy loading for npm/node
group_lazy_load $HOME/.nvm/nvm.sh node npm

# Python (pyenv) lazy loading
load_pyenv() {
  eval "$(pyenv init -)"
}

# Java (JABBA) lazy loading
alias loadjabba="source \"/Users/lamdav/.jabba/jabba.sh\""