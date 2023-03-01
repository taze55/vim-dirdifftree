" Vim global plugin for diff directory
" Maintainer: taze55 <taze_a28391214@icloud.com>

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
setlocal foldexpr=<SID>DirDiffTreeFoldExpr()

nnoremap <buffer> <silent> o             :call DirDiffTreeOpen()<CR>
nnoremap <buffer> <silent> <CR>          :call DirDiffTreeOpenOrToggleFold()<CR>
nnoremap <buffer> <silent> <2-Leftmouse> :call DirDiffTreeOpenOrToggleFold()<CR>
nnoremap <buffer> <silent> <C-N>         :call DirDiffTreeGotoNextFile()<CR>
nnoremap <buffer> <silent> <C-P>         :call DirDiffTreeGotoPreviousFile()<CR>

function! <SID>DirDiffTreeFoldExpr()
  function! <SID>StartsWithThread(thread)
    if <SID>StartsWith(s:line, a:thread)
      let s:line = s:line[len(a:thread):]
      let s:fold_level += 1
      return 1
    endif
    return 0
  endfunction

  " https://vi.stackexchange.com/questions/29062/how-to-check-if-a-string-starts-with-another-string-in-vimscript
  function! <SID>StartsWith(longer, shorter)
    return a:longer[0:len(a:shorter) - 1] ==# a:shorter
  endfunction

  let s:line = getline(v:lnum)
  let s:fold_level = 0
  let l:fold_nest_max = &foldnestmax + 1

  let l:i = 0
  while l:i < l:fold_nest_max
    if     <SID>StartsWithThread(g:DirDiffTreeThreads['blank'])
    elseif <SID>StartsWithThread(g:DirDiffTreeThreads['vertical'])
    elseif <SID>StartsWithThread(g:DirDiffTreeThreads['branch'])
    elseif <SID>StartsWithThread(g:DirDiffTreeThreads['corner'])
    else
      break
    endif
    let l:i += 1
  endwhile

  if <SID>StartsWith(s:line, '🇩 ')
    return '>' . s:fold_level
  endif

  if <SID>StartsWith(s:line, '🇫 ')
    return s:fold_level - 1
  endif

  return 0
endfunction

