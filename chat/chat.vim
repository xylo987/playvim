function! Chat_server()

python3 << EOF    

import sys
import os
import vim

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "mp3player"])

sys.path.append(pypath)
from server import Server
from threading import Thread

s = Server(23456)
Thread(target=s.start, daemon=True).start()

EOF

endfunction

function! Chat_start()

python3 << EOF    

EOF

endfunction


function! Chat_config_server()

python3 << EOF

EOF

endfunction

nmap <leader>4 :call Chat_server()<cr>
nmap <leader>5 :call Chat_start()<cr>
nmap <leader>6 :call Chat_config_server()<cr>
