" Vim global plugin for diff two directories and represent them as a tree
" Maintainer: taze55 <taze_a28391214@icloud.com>
" URL: https://github.com/taze55/vim-dirdifftree

if exists("b:did_ftplugin")
  finish
endif
let b:did_ftplugin = 1

setlocal nomodified
setlocal buftype=nofile
setlocal bufhidden=delete
setlocal noswapfile
setlocal nowrap

setlocal foldtext=getline(v:foldstart)
setlocal foldmethod=expr
setlocal foldexpr=DirDiffTreeFoldExpr()

nnoremap <buffer> <silent> o             :call dirdifftree#open()<CR>
nnoremap <buffer> <silent> <CR>          :call dirdifftree#open_or_toggle_fold()<CR>
nnoremap <buffer> <silent> <2-Leftmouse> :call dirdifftree#open_or_toggle_fold()<CR>
nnoremap <buffer> <silent> <C-N>         :call dirdifftree#goto_next_file()<CR>
nnoremap <buffer> <silent> <C-P>         :call dirdifftree#goto_previous_file()<CR>

function! DirDiffTreeFoldExpr()
  function! DirDiffTreeStartsWithThread(thread)
    if DirDiffTreeStartsWith(s:line, a:thread)
      let s:line = s:line[len(a:thread):]
      let s:fold_level += 1
      return 1
    endif
    return 0
  endfunction

  " https://vi.stackexchange.com/questions/29062/how-to-check-if-a-string-starts-with-another-string-in-vimscript
  function! DirDiffTreeStartsWith(longer, shorter)
    return a:longer[0:len(a:shorter) - 1] ==# a:shorter
  endfunction

  let s:line = getline(v:lnum)
  let s:fold_level = 0
  let l:fold_nest_max = &foldnestmax + 1

  let l:i = 0
  let l:match_threads = 0
  while l:i < l:fold_nest_max
    if     DirDiffTreeStartsWithThread(g:DirDiffTreeThreads['blank'])
    elseif DirDiffTreeStartsWithThread(g:DirDiffTreeThreads['vertical'])
    elseif DirDiffTreeStartsWithThread(g:DirDiffTreeThreads['branch'])
    elseif DirDiffTreeStartsWithThread(g:DirDiffTreeThreads['corner'])
    else
      break
    endif
    let l:match_threads = 1
    let l:i += 1
  endwhile

  " other
  if l:match_threads == 0
    return 0
  endif

  let l:dir_icon = g:DirDiffTreeIcons['dir']
  let l:file_icon = g:DirDiffTreeIcons['file']

  " dir or file
  if l:dir_icon != ''
    if DirDiffTreeStartsWith(s:line, l:dir_icon)
      return '>' . s:fold_level
    else
      return s:fold_level - 1
    endif
  elseif l:file_icon  != ''
    if DirDiffTreeStartsWith(s:line, l:file_icon)
      return s:fold_level - 1
    else
      return '>' . s:fold_level
    endif
  endif

  " difficult to discern if nothing is set on g:DirDiffTreeIcons.
  return 0
endfunction

