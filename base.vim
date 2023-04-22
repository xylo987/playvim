"
"                               基本配置
"
set nocompatible
"set cursorline
"set cursorcolumn
set encoding=utf-8
set termguicolors
set nobackup
set nowritebackup
syntax on
filetype indent on
set showmode
set showcmd
set ruler
set mouse=a
set encoding=utf-8  
set history=1000
set textwidth=79
set cc=80
set wrap
set linebreak
set scroll=10
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set autoindent
set showmatch
set hlsearch
set incsearch
set ignorecase
set smartcase
set noswapfile
set autochdir
set noerrorbells
set visualbell
set autoread
set wildmenu
set spell
set expandtab
filetype on
set helplang=cn
set autochdir
set nu

"
"                               插件列表
"
call plug#begin('~/.vim/plugged')
let g:plug_url_format = 'git@github.com:%s.git'

Plug 'scrooloose/nerdtree'
Plug 'preservim/tagbar'
Plug 'vim-airline/vim-airline'
Plug 'voldikss/vim-floaterm'
Plug 'Yggdroot/indentLine'
Plug 'vim-airline/vim-airline-themes'
Plug 'plan9-for-vimspace/acme-colors'
Plug 'altercation/vim-colors-solarized'
" Async Language Server Protocol plugin for vim8 and neovim.
Plug 'prabirshrestha/vim-lsp'
Plug 'mattn/vim-lsp-settings'
" Async autocompletion for Vim 8 and Neovim with |timers|.
Plug 'prabirshrestha/asyncomplete.vim'
Plug 'prabirshrestha/asyncomplete-lsp.vim'

Plug 'SirVer/ultisnips'
Plug 'prabirshrestha/async.vim'
Plug 'thomasfaingnaert/vim-lsp-snippets'
Plug 'thomasfaingnaert/vim-lsp-ultisnips'

" yourself ultisnips
Plug 'xylo987/vim-snippets'

Plug 'mhinz/vim-grepper', { 'on': ['Grepper', '<plug>(GrepperOperator)'] }

call plug#end()


"
"                               界面设置
"
color shine
set guioptions-=m  "menu bar
set guioptions-=T  "toolbar
set guioptions-=r  "scrollbar
set guioptions-=L  "scrollbar
hi pmenu ctermbg=white ctermfg=black guibg=white guifg=black gui=bold
hi pmenusel ctermbg=gray ctermfg=white guibg=gray guifg=white gui=bold
hi colorcolumn guibg=lightgrey
hi folded ctermbg=gray ctermfg=black guibg=gray guifg=black gui=bold
hi cursorline ctermbg=gray ctermfg=black guibg=gray guifg=black
hi cursorcolumn ctermbg=gray ctermfg=black guibg=gray guifg=black
hi Floaterm guibg=white guifg=black ctermbg=white ctermfg=black
hi FloatermBorder guibg=pink guifg=gray
set fillchars=vert:\|,fold:\-,eob:\ 
hi VertSplit term=none cterm=none gui=none guibg=black guifg=white
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
let g:NERDTreeDirArrowExpandable = '-'
let g:NERDTreeDirArrowCollapsible = '<'
let g:airline_theme='base16_adwaita'
let g:floaterm_height = 0.3
let g:floaterm_width = 0.99
let g:floaterm_position = 'bottom'
let g:floaterm_title = 'love($1/$2)'
hi SpellBad ctermfg=015 ctermbg=000 cterm=none guifg=#FFFFFF guibg=#000000 gui=none



"
"                               按键设置
"
function! Run()
    let ext = expand('%:e')

    if ext  == 'py'
        exec ('FloatermNew --autoclose=0 python3 %')
    elseif ext  == 'rs'
        if has('nvim')
            exec 'FloatermNew --autoclose=0 --wintype=popup rustc % -o %< && ./%<'
        else
            exec 'FloatermNew! --autoclose=0 --wintype=popup rustc % -o %< && ./%<'
        endif
    else
        echo 'file not supported: '.expand('%:t')
    endif
endfunction

function! ConfigFile()
    find $HOME/.vim_runtime/README.md
endfunction

function! SnippetsFile()
    find $HOME/.vim/plugged/vim-snippets/README.md
endfunction


let g:mapleader = ","
nmap <F1> :call ConfigFile()<cr>
nmap <F2> :NERDTreeToggle<cr>
nmap <F3> :TagbarToggle<cr>
nmap <F4> :call SnippetsFile()<cr>
nmap <F5> :call Run()<cr>
" F6 调试命令等待好的插件出现
let g:floaterm_keymap_new    = '<F7>'
let g:floaterm_keymap_prev   = '<F8>'
let g:floaterm_keymap_next   = '<F9>'
let g:floaterm_keymap_kill   = '<F10>'
" F11 暂不设置
let g:floaterm_keymap_toggle = '<F12>'
nmap <leader>r :NERDTreeFind<cr>
" python3的home环境变量
let &pythonthreehome="/Library/Frameworks/Python.framework/Versions/3.11/"
