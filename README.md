# vim-dirdifftree

DirDiffTree plugin for Vim

Diff two directories and represent them as a tree

<!-- ![DirDiffTree screenshot](./image/screenshot.png) -->

## Installation

With [pathogen.vim](https://github.com/tpope/vim-pathogen):

    cd ~/.vim/bundle
    git clone git://github.com/taze55/vim-dirdifftree

With [vim-plug](https://github.com/junegunn/vim-plug), in your ~/.vimrc:

    Plug 'taze55/vim-dirdifftree'

With Vim 8+'s default packaging system:

    mkdir -p ~/.vim/pack/bundle/start
    cd ~/.vim/pack/bundle/start
    git clone git://github.com/taze55/vim-dirdifftree

## Usage

    :DirDiffTree <dir1> <dir2>

To open DirDiffTree from the command line, run `vim -c "DirDiffTree dir1 dir2"`

## License

```
Copyright (c) 2023 taze55
Released under the MIT license
https://opensource.org/license/mit/
```
