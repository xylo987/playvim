function! Self_mp3server_start()

python3 << EOF

import sys
import os
import vim

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "self_plugins"])

sys.path.append(pypath)

from threading import Thread
from mp3player_server import Mp3Server

s = Mp3Server()
t = Thread(target=s.main, daemon=True)
t.start()

EOF

endfunction


nmap <leader>1 :call Self_mp3server_start()<cr>


function! Self_mp3client_send()

python3 << EOF

import sys
import os
import vim

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "self_plugins"])

sys.path.append(pypath)

from threading import Thread
from mp3player_client import Mp3Client

c = Mp3Client()
cmd = vim.eval(('input("请输入命令以控制音乐盒子'
                '[start,stop,next,prev,pause,unpause,quit]：")'))
if cmd not in ['start','stop','prev','next','pause','unpause','quit']:
    print('命令不正确')
else:
    c.send(cmd)

EOF

endfunction


nmap <leader>2 :call Self_mp3client_send()<cr>
