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
import socket

s = socket.socket()
try:
    s.connect(('localhost', 12345))
    print('天天音乐已启动')
    s.close()
except:
    s = Mp3Server()
    t = Thread(target=s.main, daemon=True)
    t.start()

EOF

endfunction

function! Self_mp3server_web()

python3 << EOF

import sys
import os
import vim
import asyncio

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "self_plugins"])

sys.path.append(pypath)

from threading import Thread
from mp3player_web import main
import socket
from webbrowser import open

s = socket.socket()
try:
    s.connect(('localhost', 12346))
    print('天天音乐后台启动')
    s.close()
except:
    w = Thread(target=asyncio.run, args=(main(),), daemon=True)
    w.start()
    open('http://localhost:12346')

EOF

endfunction

nmap <leader>1 :call Self_mp3server_start()<cr>
nmap <leader>3 :call Self_mp3server_web()<cr>


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

vim.command('messages clear')
c = Mp3Client()
cmd = vim.eval(('input("请输入命令以控制音乐盒子'
                '[start,stop,next,prev,pause,unpause'
                ',quit,list,play_index]:")'))
vim.command('echo "\n"')
c.send(cmd)

EOF

endfunction


nmap <leader>2 :call Self_mp3client_send()<cr>
