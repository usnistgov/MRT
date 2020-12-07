#prevent wine from adding menuitems and desktop shortkuts
WINEDLLOVERRIDES=winemenubuilder.exe=d

# Check for an interactive session
[ -z "$PS1" ] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias supac='sudo pacman'
alias psync='sudo pacman -Sy'
alias :q='exit'
alias maxima='rmaxima'

# don't put duplicate lines in the history. See bash(1) for more options
export HISTCONTROL=ignoredups
# ... and ignore same sucessive entries.
export HISTCONTROL=ignoreboth

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

#check for remote sessions and show host in prompt
if [ -z "$SSH_CLIENT" ]
then
    #local session
    PS1='\[\e[0;32m\]\u\[\e[0m\] \[\e[1;34m\]\w\[\e[0m\] \[\e[1;32m\]$\[\e[0m\] '
else
    #SSH sesion
    PS1='\[\e[0;32m\]\u\[\e[0m\]@\[\e[0;31m\]\h\[\e[0m\] \[\e[1;34m\]\w\[\e[0m\] \[\e[1;32m\]$\[\e[0m\] '
fi

complete -cf sudo
export EDITOR="vim"
export VISUAL="vim"

#color man pages
man() {
    env LESS_TERMCAP_mb=$(printf "\e[1;31m") \
	LESS_TERMCAP_md=$(printf "\e[1;31m") \
	LESS_TERMCAP_me=$(printf "\e[0m") \
	LESS_TERMCAP_se=$(printf "\e[0m") \
	LESS_TERMCAP_so=$(printf "\e[1;44;33m") \
	LESS_TERMCAP_ue=$(printf "\e[0m") \
	LESS_TERMCAP_us=$(printf "\e[1;32m") \
	man "$@"
}

set -o vi



