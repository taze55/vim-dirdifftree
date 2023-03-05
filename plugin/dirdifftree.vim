" Vim global plugin for diff two directories and represent them as a tree
" Maintainer: taze55 <taze_a28391214@icloud.com>
" URL: https://github.com/taze55/vim-dirdifftree

if exists('g:loaded_dirdifftree')
  finish
endif
let g:loaded_dirdifftree = 1

" Public Interface:
command! -nargs=* -complete=dir DirDiffTree call dirdifftree#execute(<f-args>)

" Event
augroup DirDiffTree
  autocmd!
  autocmd BufDelete DirDiffTree* call dirdifftree#cleanup(expand('<abuf>'))
augroup end
