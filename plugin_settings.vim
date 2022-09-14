" vim-lsp: 1, vim-lsp-settings: 2, asyncomplete: 3
let g:lsp_fold_enabled = 0 " 禁用插件全局折叠代码
    " 1. 调试信息
    let g:lsp_log_verbose = 1
    let g:lsp_log_file = expand('~/vim-lsp.log')

    " 3. 调试信息
    let g:asyncomplete_log_file = expand('~/asyncomplete.log')

    " 1. 代码跳转
    nmap <leader>gd :LspDefinition<cr>
