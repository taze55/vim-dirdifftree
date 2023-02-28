# vim-dirdifftree

DirDiffTree plugin for Vim

Diff two directories and represent them as a tree

<!-- ![DirDiffTree screenshot](./image/screenshot.png) -->

## Installation

With [pathogen.vim](https://github.com/tpope/vim-pathogen):

```sh
cd ~/.vim/bundle
git clone git://github.com/taze55/vim-dirdifftree
```

With [vim-plug](https://github.com/junegunn/vim-plug), in your ~/.vimrc:

```vim
Plug 'taze55/vim-dirdifftree'
```

With Vim 8+'s default packaging system:

```sh
mkdir -p ~/.vim/pack/bundle/start
cd ~/.vim/pack/bundle/start
git clone git://github.com/taze55/vim-dirdifftree
```

## Usage

```vim
:DirDiffTree <dir1> <dir2>
```

To open DirDiffTree from the command line, run `vim -c "DirDiffTree dir1 dir2"`

## Syntax highlighting

The following highlight groups are available.

```vim
DirDiffTreeComment      " default links to Comment
DirDiffTreeTopDirectory " default links to Title
DirDiffTreeThread       " default links to Comment
DirDiffTreeDirectory    " default links to Directory
DirDiffTreeAdd          " default links to PreProc
DirDiffTreeDelete       " default links to PreProc
DirDiffTreeSelected     " default links to Visual
```

You can overwrite these highlight groups in your colorscheme.

## License

```
Copyright (c) 2023 taze55
Released under the MIT license
https://opensource.org/license/mit/
```
