" Vim global plugin for diff two directories and represent them as a tree
" Maintainer: taze55 <taze_a28391214@icloud.com>
" URL: https://github.com/taze55/vim-dirdifftree

if exists("b:current_syntax")
  finish
endif

let s:save_cpo = &cpoptions
set cpoptions&vim

syn region DirDiffTreeComment oneline start="//" end="$" contains=DirDiffTreeUsage
syn region DirDiffTreeUsage matchgroup=DirDiffTreeComment oneline start="Usage: " end="$" contained keepend contains=@DirDiffTreeUsageGroup
syn match  DirDiffTreeUsageCmd "\s*\zs[^,:]\+\ze:" contained
syn match  DirDiffTreeUsageSep1 ":" contained
syn match  DirDiffTreeUsageNote "\s*\zs[^,:]\+\ze\(,\|$\)" contained
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
exe 'syn match  DirDiffTreeThread "' . DirDiffTreeThreadRegex() . '"'
let s:dir_icon = DirDiffTreeEscapeForVimRegexp(g:DirDiffTreeIcons['dir'])
if s:dir_icon != ''
  exe 'syn match  DirDiffTreeDirectory "' . s:dir_icon . '\zs.\+" contains=DirDiffTreeAdd,DirDiffTreeDelete'
endif
syn match  DirDiffTreeAdd "\[+\]$"
syn match  DirDiffTreeDelete "\[-\]$"

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
