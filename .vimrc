set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
  Plugin 'VundleVim/Vundle.vim'
  Plugin 'scrooloose/nerdtree' 
  Plugin 'bling/vim-airline'
  Plugin 'airblade/vim-gitgutter'
  Plugin 'tomasr/molokai'
call vundle#end()

map <F2> :NERDTreeToggle<CR>

set ai
set cul
set expandtab
set history=200
set hlsearch
set ignorecase
set incsearch
set noerrorbells
set number
set ruler
set scrolloff=5
set shiftwidth=2
set showmatch
set softtabstop=2
set t_vb=
set visualbell
set autoindent
set tabstop=2
set laststatus=2
colorscheme molokai
syntax on
autocmd FileType make setlocal noexpandtab

:imap jj <Esc>
