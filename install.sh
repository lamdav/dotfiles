#!/usr/bin/env bash

export dir="$(pwd)"

# install brew
echo "installing homebrew\n"
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update && brew upgrade && brew bundle

# install rvm
echo "installing rvm\n"
curl -sSL https://get.rvm.io | bash -s stable

# install oh-my-zsh (zsh easy install)
echo "installing zsh shell\n"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
rm -rf ~/.zshrc && ln -sf $dir/.zshrc ~/.zshrc
rm -rf ~/.zsh_plugins && ln -sf $dir/.zsh_plugins ~/.zsh_plugins
rm -rf ~/.zlogin && ln -sf $dir/.zlogin ~/.zlogin
mkdir -p ~/.oh-my-zsh/custom/themes
ln -sf steeef-lambda.zsh-theme ~/.oh-my-zsh/custom/themes/steeef-lambda.zsh-theme
rm -rf ~/.p10k.zsh && ln -sf $dir/.p10k.zsh ~/.p10k.zsh
source ~/.zshrc
updateplugins
echo "run when completed: exec zsh\n"

# setup vim
echo "setting up vim\n"
rm -rf ~/.vimrc && ln -sf $dir/.vimrc ~/.vimrc

# setup git configurations
echo "setting up gitconfig\n"
rm -rf ~/.gitconfig && ln -sf $dir/.gitconfig ~/.gitconfig

# setup iterm2 profile (dynamic)
echo "setting up iterm2 profile\n"
mkdir -p ~/Library/Application\ Support/iTerm2/DynamicProfiles
ln -sf $dir/iterm-profiles.json ~/Library/Application\ Support/iTerm2/DynamicProfiles/iterm-profiles.json
# prompts user to add color scheme
open firewatch.itermcolors
