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
rm -rf ~/.zshrc && cp .zshrc ~/.zshrc
cp steeef-lambda ~/.oh-my-zsh/custom/themes/steeef-lambda.zsh-theme
source ~/.zshrc

# setup vim
echo "setting up vim\n"
rm -rf ~/.vimrc && cp .vimrc ~/.vimrc

