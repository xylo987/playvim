function! Chat_server()

python3 << EOF    

import sys
import os
import vim

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "chat"])

sys.path.append(pypath)
from server import Server
from threading import Thread
import socket

s = None
port = 23456
try:
    s = socket.socket()
    s.connect(('localhost', 23456))
except Exception as e:
    s = Server(port)
    Thread(target=s.start, daemon=True).start()
finally:
    print('聊天服务器已启动')
    try:
        s.close()
    except Exception as e:
        print(e)

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
