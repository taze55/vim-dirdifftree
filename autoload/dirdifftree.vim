" Vim global plugin for diff two directories and represent them as a tree
" Maintainer: taze55 <taze_a28391214@icloud.com>
" URL: https://github.com/taze55/vim-dirdifftree

" Options
if !exists("g:DirDiffTreeMainWindowWidth")
    let g:DirDiffTreeMainWindowWidth = 56
endif

if !exists("g:DirDiffTreeNoneFileWindowWidth")
    let g:DirDiffTreeNoneFileWindowWidth = 32
endif

if !exists("g:DirDiffTreeThreads")
    let g:DirDiffTreeThreads = {'blank': '    ', 'vertical': '│  ', 'branch': '├─', 'corner': '└─'}
endif

if !exists("g:DirDiffTreeIcons")
  if has('osxdarwin')
    let g:DirDiffTreeIcons = {'dir': '🇩 ', 'file': '🇫 '}
  else
    let g:DirDiffTreeIcons = {'dir': '[D]', 'file': ''}
  endif
endif

if !exists("g:DirDiffTreeExcludeDirs")
    let g:DirDiffTreeExcludeDirs = ['.git', 'node_modules', '__pycache__']
endif

if !exists("g:DirDiffTreeIgnoreCase")
    let g:DirDiffTreeIgnoreCase = 1
endif

py3 import dirdifftree

function! dirdifftree#execute(left, right) abort
  py3 dirdifftree.dirDiffTreeExecute(vim.eval("a:left"), vim.eval("a:right"))
endfunction

function! dirdifftree#open_or_toggle_fold() abort
  py3 dirdifftree.dirDiffTreeOpenOrToggleFold()
endfunction

function! dirdifftree#open() abort
  py3 dirdifftree.dirDiffTreeOpen()
endfunction

function! dirdifftree#toggle_fold() abort
  py3 dirdifftree.dirDiffTreeToggleFold()
endfunction

function! dirdifftree#goto_next_file()
  py3 dirdifftree.dirDiffTreeGotoNextFile()
endfunction

function! dirdifftree#goto_previous_file() abort
  py3 dirdifftree.dirDiffTreeGotoPreviousFile()
endfunction

function! dirdifftree#cleanup(abuf) abort
  py3 dirdifftree.dirDiffTreeCleanUp(vim.eval("a:abuf"))
endfunction

