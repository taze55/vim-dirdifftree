" Vim global plugin for diff directory
" Maintainer: taze55 <taze_a28391214@icloud.com>

if exists('g:loaded_dirdifftree')
  finish
endif
let g:loaded_dirdifftree = 1

py3 import dirdifftree

" Public Interface:
command! -nargs=* -complete=dir DirDiffTree call DirDiffTreeExecute(<f-args>)

" Event
augroup DirDiffTree
  autocmd!
  autocmd BufDelete DirDiffTree* call DirDiffTreeCleanUp(expand('<abuf>'))
augroup end

function! DirDiffTreeExecute(left, right)
  py3 dirdifftree.dirDiffTreeExecute(vim.eval("a:left"), vim.eval("a:right"))
endfunction

function! DirDiffTreeOpenOrToggleFold()
  py3 dirdifftree.dirDiffTreeOpenOrToggleFold()
endfunction

function! DirDiffTreeOpen()
  py3 dirdifftree.dirDiffTreeOpen()
endfunction

function! DirDiffTreeToggleFold()
  py3 dirdifftree.dirDiffTreeToggleFold()
endfunction

function! DirDiffTreeGotoNextFile()
  py3 dirdifftree.dirDiffTreeGotoNextFile()
endfunction

function! DirDiffTreeGotoPreviousFile()
  py3 dirdifftree.dirDiffTreeGotoPreviousFile()
endfunction

function! DirDiffTreeCleanUp(abuf)
  py3 dirdifftree.dirDiffTreeCleanUp(vim.eval("a:abuf"))
endfunction

