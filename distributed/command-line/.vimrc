" Use Vim settings, rather than Vi settings (much better!).
set nocompatible

" allow backspacing over everything in insert mode
set backspace=indent,eol,start

set nobackup      " do not keep a backup file, use versions instead

filetype plugin indent on
syntax on

" set syntax settings for C
let c_gnu = 1
let c_space_errors=1
let c_no_bracket_error=1
let c_no_curly_error = 1
let c_syntax_for_h = 1

" set dfault shell to bash
let g:is_bash = 1
let g:sh_fold_enabled = 4

au BufRead,BufNewFile PKGBUILD          
            \if &ft == 'sh' |
            \set ft=pkgbuild |
            \set syn=sh |
            \endif

set modeline        " Enable modelines

set number

set wrap
set linebreak
 
set hlsearch        " When there is a previous search pattern, highlight all
                    " its matches.
 
set incsearch       " While typing a search command, show immediately where the
                    " so far typed pattern matches.

set showcmd         " display incomplete commands
 
" CTRL-U in insert mode deletes a lot.  Use CTRL-G u to first break undo,
" so that you can undo CTRL-U after inserting a line break.
inoremap <C-U> <C-G>u<C-U>

set ignorecase      " Ignore case in search patterns.
 
set smartcase       " Override the 'ignorecase' option if the search pattern
                    " contains upper case characters.
set autoindent

set ruler

set background=dark

"tabbing options use space instead of tabs for all but makefiles

set expandtab
set softtabstop=4

set tabstop=4
set shiftwidth=4

autocmd FileType make setlocal noexpandtab

" fix anoying features of vim-latex
let g:Tex_SmartKeyBS = 0
let g:Tex_SmartKeyQuote = 0
let g:Tex_SmartKeyDot = 0
let g:Imap_UsePlaceHolders = 0
let g:Tex_Leader = '`tex'
let g:Tex_Leader2 = ',tex'
"some more fixes sugested, not sure how to use them though
"call IMAP('()', '()', 'tex')
"call IMAP('{}', '{}', 'tex')
"call IMAP('[]', '[]', 'tex')
"call IMAP('::', '::', 'tex')
"call IMAP('{{', '{{', 'tex')
"call IMAP('((', '((', 'tex')
"call IMAP('[[', '[[', 'tex')
"call IMAP('$$', '$$', 'tex')

"command for generating integrity checks for pakcage build files
"if &ft == 'pkgbuild'
    command-buffer Integ r! makepkg -g 2>/dev/null
    "command Integ /md5sums | d/)x | r! makepkg -g 2>/dev/null
"endif

command-buffer Mod r! hwdetect --modules


" code folding options

set nofen       "unfold all folds

"set fen

set foldmethod=syntax
"python needs fdm=indent because it is funny like that
autocmd FileType python setlocal foldmethod=indent

"set foldlevel=0
"foldopen
"set foldcolumn=6

" When editing a file, always jump to the last known cursor position.
" Don't do it when the position is invalid or when inside an event handler
" (happens when dropping a file on gvim).
" Also don't do it when the mark is in the first line, that is the default
" position when opening a file.
autocmd BufReadPost *
\ if line("'\"") > 1 && line("'\"") <= line("$") |
\   exe "normal! g`\"" |
\ endif

" Convenient command to see the difference between the current buffer and the
" file it was loaded from, thus the changes you made.
" Only define it when not defined already.
if !exists(":DiffOrig")
command DiffOrig vert new | set bt=nofile | r # | 0d_ | diffthis
      \ | wincmd p | diffthis
endif

" Synctex for thesis
" TODO: figure out how to make this more general
command Synctex echo system('synctex view -i '.shellescape(printf("%d:%d:%s",line("."),0,bufname("%s"))).' -o thesis.pdf')

"set encryption to use blowfish for better encryption
set cm=blowfish

"when using encryption turn off backups and swap
"this prevents unencrypted files from being written to disk
if !empty(&key)|
    setlocal nobackup
    setlocal noswapfile
    setlocal nowritebackup
endif
