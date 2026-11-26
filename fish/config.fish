if status is-interactive
# Commands to run in interactive sessions can go here
set -g fish_greeting

starship init fish | source

# alias
alias ls "lsd --group-directories-first"
alias grep "grep --color=auto"
alias pacman "pacman --color=auto"
alias paru "paru --color=auto"
alias diff "diff --color=auto"
alias code "/usr/bin/codium"

fastfetch

end


# Added by Antigravity CLI installer
set -gx PATH "/home/nik/.local/bin" $PATH
