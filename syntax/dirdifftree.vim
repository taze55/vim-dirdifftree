" Vim global plugin for diff directory
" Maintainer: taze55 <taze_a28391214@icloud.com>

if exists("b:current_syntax")
  finish
endif

let s:save_cpo = &cpoptions
set cpoptions&vim

syn region DirDiffTreeComment oneline start="//" end="$" contains=DirDiffTreeUsage
syn region DirDiffTreeUsage matchgroup=DirDiffTreeComment oneline start="Usage: " end="$" contained keepend contains=@DirDiffTreeUsageGroup
syn match  DirDiffTreeUsageCmd "\s*\zs[^,:]\+\ze:" contained nextgroup=DirDiffTreeUsageSep1
syn match  DirDiffTreeUsageSep1 ":" contained nextgroup=DirDiffTreeUsageNote
syn match  DirDiffTreeUsageNote "\s*\zs[^,:]\+\ze\(,\|$\)" contained nextgroup=DirDiffTreeUsageSep2
syn match  DirDiffTreeUsageSep2 "," contained
syn cluster DirDiffTreeUsageGroup contains=DirDiffTreeUsageCmd,DirDiffTreeUsageSep1,DirDiffTreeUsageNote,DirDiffTreeUsageSep2

function! DirDiffTreeThreadRegex()
  let l:concatenate =
\ '^\(' . DirDiffTreeEscapeForVimRegexp(g:DirDiffTreeThreads['blank']) .
\ '\|'  . DirDiffTreeEscapeForVimRegexp(g:DirDiffTreeThreads['vertical']) .
\ '\|'  . DirDiffTreeEscapeForVimRegexp(g:DirDiffTreeThreads['branch']) .
\ '\|'  . DirDiffTreeEscapeForVimRegexp(g:DirDiffTreeThreads['corner']) . '\)\+'
  return l:concatenate
endfunction

" https://stackoverflow.com/questions/11311431/how-to-escape-search-patterns-or-regular-expressions-in-vimscript
" char '?' does not need to be escaped
function! DirDiffTreeEscapeForVimRegexp(str)
  return escape(a:str, '^$.*/\[]~')
endfunction

syn region DirDiffTreeTopDirectory oneline start="^\%3l\%1c" end="$"
exe 'syn match  DirDiffTreeThread "' . DirDiffTreeThreadRegex() . '" nextgroup=DirDiffTreeDirectory'
syn match  DirDiffTreeDirectory "🇩 \zs.\+" contains=DirDiffTreeAdd,DirDiffTreeDelete
syn match  DirDiffTreeAdd "\[+\]"
syn match  DirDiffTreeDelete "\[-\]"

hi def link DirDiffTreeComment      Comment
hi def link DirDiffTreeUsage        DirDiffTreeComment
hi def link DirDiffTreeTopDirectory Title
hi def link DirDiffTreeThread       Comment
hi def link DirDiffTreeDirectory    Directory
hi def link DirDiffTreeAdd          PreProc
hi def link DirDiffTreeDelete       PreProc
hi def link DirDiffTreeSelected     Visual
hi def link DirDiffTreeFailed       Error
hi def link DirDiffTreeUsageCmd     Function
hi def link DirDiffTreeUsageSep1    Delimiter
hi def link DirDiffTreeUsageNote    Normal
hi def link DirDiffTreeUsageSep2    DirDiffTreeComment

let b:current_syntax = "dirdifftree"

let &cpoptions = s:save_cpo
unlet s:save_cpo
