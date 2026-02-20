# Lazy Loading Functions for Better Performance
# Note: Node, Python, and Java version management is handled by mise (see 99_integrations.zsh)

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
