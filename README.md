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

## Options

The following options are available.

| Options                          | Default value | Type    |
| -------------------------------- | ------------- | ------- |
| g:DirDiffTreeMainWindowWidth     | 64            | Integer |
| g:DirDiffTreeNoneFileWindowWidth | 32            | Integer |

## Syntax highlighting

The following highlight groups are available.

| Highlight groups        | Default link |
| ----------------------- | ------------ |
| DirDiffTreeTopDirectory | Title        |
| DirDiffTreeThread       | Comment      |
| DirDiffTreeDirectory    | Directory    |
| DirDiffTreeAdd          | PreProc      |
| DirDiffTreeDelete       | PreProc      |
| DirDiffTreeSelected     | Visual       |

You can overwrite these highlight groups in your colorscheme.

## License

```
Copyright (c) 2023 taze55
Released under the MIT license
https://opensource.org/license/mit/
```
