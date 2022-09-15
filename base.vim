"
"                               基本配置
"
set nocompatible
set cursorline
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
"set spell
set expandtab
filetype on



"
"                               插件列表
"
call plug#begin('~/.vim/plugged')

Plug 'scrooloose/nerdtree'
Plug 'preservim/tagbar'
Plug 'vim-airline/vim-airline'
Plug 'voldikss/vim-floaterm'
Plug 'Yggdroot/indentLine'
Plug 'vim-airline/vim-airline-themes'
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
Plug 'syz-lm/vim-snippets'

call plug#end()


"
"                               界面设置
"
color murphy
set guioptions-=m  "menu bar
set guioptions-=T  "toolbar
set guioptions-=r  "scrollbar
set guioptions-=L  "scrollbar
hi pmenu ctermbg=white ctermfg=black guibg=white guifg=black gui=bold
hi pmenusel ctermbg=gray ctermfg=white guibg=gray guifg=white gui=bold
hi colorcolumn guibg=yellow
hi folded ctermbg=gray ctermfg=black guibg=gray guifg=black gui=bold
hi cursorline ctermbg=green ctermfg=black guibg=green guifg=black
hi cursorcolumn ctermbg=green ctermfg=black guibg=green guifg=black
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
    edit $HOME/.vim_runtime/__init__.vim
endfunction


let g:mapleader = ","
nmap <F1> :call ConfigFile()<cr>
nmap <F2> :NERDTreeToggle<cr>
nmap <F3> :TagbarToggle<cr>
" F4 预览命令等待好的插件出现
nmap <F5> :call Run()<cr>
" F6 调试命令等待好的插件出现
let g:floaterm_keymap_new    = '<F7>'
let g:floaterm_keymap_prev   = '<F8>'
let g:floaterm_keymap_next   = '<F9>'
let g:floaterm_keymap_kill   = '<F10>'
" F11 暂不设置
let g:floaterm_keymap_toggle = '<F12>'



"
"                                总结
"
" 很多插件都不好用，很讨厌哪种，为了安装一个功能却要安装很多插件和另外的可执行
" 程序的插件，插件就不能做成，比如专门做补全的，专门做跳转代码的，专门做文档的
" 预览的，也是不知道为什么，现在的插件总是各种问题，抱歉，我没有那个时间去学习
" VIM插件相关的开发，市面上也没有这类的资料，就没有一款比较全面的介绍。
"
" 所以，VIM我就用来当编辑器中的玩具了。
"
" RUST语言不知道多坑，乱七八糟的，要我看，还不如C++来的舒服。做业务比不过Java
" 做小项目速度比不过Python，做系统软件比不过C++/C，老师总是跟我们讲，不要搞世界
" 上已经存在的行业，况且，C/C++，Java，Python，Javascript目前在业界，基本吃完一
" 切，现在只不过在夕阳之际，现在要出来分一杯羹，和传统巨头技术去卷罢了。
"
" 让我看，做程序员，还是老老实实把这4们编程语言学好，其它的不看也罢，如果图省事
" 就学个C，Python，Javascript也行。就已经够混饭了，后面就是算法和基础了，基础一
" 半在C里面，做应用，Python，Javascript都能搞定，未来的时间不多了，学Rust其它就
" 像在炒作的语言，就像在无脑跟风一样。
"
" 当然，有人会说，新技术比老技术好，但是让我们想想，我们现在的信息软件科技，都
" 是由这些4们语言构建起来，这么多上线的，成功的应用，足以证明我的总结相当到位，
" 
" VIM是个好的编辑器，我只能说这么多，古老的编辑器。
"
" 未来，如果出现了代码非常精简，功能简单直接的插件，我还是会去研究的，但是，目
" 前，遇到的还太少。
"
" :joy:
" Good luck!
"
