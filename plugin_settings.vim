" vim-lsp: 1, vim-lsp-settings: 2, [asyncomplete, asyncomplete-lsp]: 3
"
    " 1. 折叠太卡了
    let g:lsp_fold_enabled = 0
    set foldmethod=expr
        \ foldexpr=lsp#ui#vim#folding#foldexpr()
        \ foldtext=lsp#ui#vim#folding#foldtext()
    " 1. 调试信息
    let g:lsp_log_verbose = 1
    let g:lsp_log_file = expand('$HOME/vim-lsp.log')

    " 3. 调试信息
    let g:asyncomplete_log_file = expand('$HOME/asyncomplete.log')

    " 1. 代码跳转
    nmap <C-]> :LspDefinition<cr>
    
    " 3. 补全
    inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
    inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
    inoremap <expr> <cr>    pumvisible() ? asyncomplete#close_popup() : "\<cr>"
"
"


" vim-lsp-ultisnips: 1
"
    " 1.代码片段补全
    let g:UltiSnipsExpandTrigger="<tab>"
    let g:UltiSnipsJumpForwardTrigger="<c-b>"
    let g:UltiSnipsJumpBackwardTrigger="<c-z>"

    set completeopt+=menuone
"
"
