#!/usr/bin/env bash

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
rm -rf ~/.zshrc && ln -sf .zshrc ~/.zshrc
mkdir -p ~/.oh-my-zsh/custom/themes
ln -sf steeef-lambda.zsh-theme ~/.oh-my-zsh/custom/themes/steeef-lambda.zsh-theme
rm -rf ~/.purepower && ln -sf .purepower ~/.purepower
source ~/.zshrc
updateplugins
echo "run when completed: exec zsh\n"

# setup vim
echo "setting up vim\n"
rm -rf ~/.vimrc && ln -sf .vimrc ~/.vimrc

# setup git configurations
echo "setting up gitconfig\n"
rm -rf ~/.gitconfig && ln sf .gitconfig ~/.gitconfig

# setup iterm2 profile (dynamic)
echo "setting up iterm2 profile\n"
mkdir -p ~/Library/Application\ Support/iTerm2/DynamicProfiles
cp iterm-profiles.json ~/Library/Application\ Support/iTerm2/DynamicProfiles/
# prompts user to add color scheme
open firewatch.itermcolors
