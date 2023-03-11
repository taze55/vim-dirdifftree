# vim-dirdifftree

DirDiffTree plugin for Vim

Diff two directories and represent them as a tree

![DirDiffTree screenshot](https://vim-dirdifftree.s3.ap-northeast-1.amazonaws.com/screenshot.png)

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

## Requirement

DirDiffTree requires python 3.8.10 or later to work. Install as needed.

## Usage

```vim
:DirDiffTree <dir1> <dir2>
```

To open DirDiffTree from the command line, run `vim -c "DirDiffTree dir1 dir2"`

## Configuration in Git

If you want to use it with git difftool, you can set it in .gitconfig as follows (this is an example of a configuration)

```
[diff]
  tool = vimdiff

[difftool "vimdiff"]
  cmd = vim -c \"DirDiffTree \"$LOCAL\" \"$REMOTE\"\"

[alias]
  showtool = "!showci () { rev=${1:-HEAD}; git difftool -d $rev~1 $rev; }; showci $1"
```

Then you can do the following

```sh
git difftool
```

or

```sh
git showtool
```

## Options

The following options are available.

| Options                          | Default                                                                                    | Description                                                                                                                                   |
| -------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| g:DirDiffTreeMainWindowWidth     | 56                                                                                         |                                                                                                                                               |
| g:DirDiffTreeNoneFileWindowWidth | 32                                                                                         | Not used below 0                                                                                                                              |
| g:DirDiffTreeThreads             | `{'blank': '    ', 'vertical': '│  ', 'branch': '├─', 'corner': '└─'}`                     |                                                                                                                                               |
| g:DirDiffTreeIcons               | macOS<br /> `{'dir': '🇩 ', 'file': '🇫 '}`<br />others<br /> `{'dir': '[D]', 'file': ''}` | Syntax hightlighing group "DirDiffTreeDirectory" does not work if 'dir' is empty'. If 'dir' and 'file' are both empty, folding does not work. |
| g:DirDiffTreeExcludeDirs         | `['.git', 'node_modules', '__pycache__']`                                                  |                                                                                                                                               |
| g:DirDiffTreeIgnoreCase          | 1                                                                                          | Not used for comparison with excluded directories                                                                                             |

## Mapping

If you want to set up Mapping, you can do so in `~/.vim/after/ftplugin/dirdifftree.vim`, etc. as follows

```vim
nmap <buffer> <silent> <Down> <C-N>o
nmap <buffer> <silent> <Up>   <C-P>o
```

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
