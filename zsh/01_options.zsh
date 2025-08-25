# ZSH Options and Behavior Configuration

# History configuration
HISTFILE="${HOME}/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000
setopt extended_history          # record timestamp of command in HISTFILE
setopt hist_expire_dups_first    # delete duplicates first when HISTFILE size exceeds HISTSIZE
setopt hist_ignore_all_dups      # ignore duplicated commands history list
setopt hist_ignore_space         # ignore commands that start with space
setopt hist_verify               # show command with history expansion to user before running it
setopt inc_append_history        # add commands to HISTFILE in order of execution
setopt share_history             # share command history data

# Directory navigation
setopt auto_cd                   # if command is a directory, cd into it
setopt auto_pushd                # make cd push old directory to directory stack
setopt pushd_ignore_dups         # don't push multiple copies of same directory
setopt pushd_minus               # exchanges meanings of +/- when navigating directory stack

# Completion behavior
setopt auto_menu                 # show completion menu on successive tab press
setopt complete_in_word          # complete from both ends of a word
setopt always_to_end             # move cursor to end of word after completion
unsetopt menu_complete           # don't autoselect the first completion entry
unsetopt flowcontrol            # disable start/stop characters (^S/^Q)

# Globbing and expansion
setopt extended_glob             # enable extended globbing syntax
setopt glob_dots                 # include dotfiles in globbing
setopt no_case_glob             # case insensitive globbing
setopt numeric_glob_sort        # sort filenames numerically when it makes sense

# Error handling and safety
unsetopt correct                 # disable spelling correction of commands
setopt no_clobber               # don't overwrite existing files with > redirect

# Job control
setopt long_list_jobs           # list jobs in long format by default
setopt notify                   # report status of background jobs immediately