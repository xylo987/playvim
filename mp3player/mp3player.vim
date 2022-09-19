function! Self_mp3server_start()

python3 << EOF

import sys
import os
import vim

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "mp3player"])

sys.path.append(pypath)

from threading import Thread
try:
    from mp3player_server import Mp3Server
except:
    pyhome = vim.eval('expand(pythonthreehome)')   
    pip_bin = os.path.sep.join([pyhome, 'bin', 'python3'])
    trust = ('-i https://pypi.doubanio.com/simple/'
             ' --trusted-host pypi.doubanio.com')
    mds = 'pygame tornado'
    vim.command('!%s -m pip install %s %s' % (
                pip_bin, mds, trust))
    print('出现错误，请重启vim再加载配置触发安装依赖程序')
    print('安装成功，也请重启使之生效')


try:
    s = Mp3Server()
    t = Thread(target=s.main, daemon=True)
    t.start()
    print('mp3服务器已启动')
except Exeption as e:
    print(e)

EOF

endfunction

function! Self_mp3server_web()

python3 << EOF

import sys
import os
import vim
import asyncio

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "mp3player"])

sys.path.append(pypath)

from threading import Thread
try:
    from mp3player_web import main
except:
    pyhome = vim.eval('expand(pythonthreehome)')   
    pip_bin = os.path.sep.join([pyhome, 'bin', 'python3'])
    trust = ('-i https://pypi.doubanio.com/simple/'
             ' --trusted-host pypi.doubanio.com')
    mds = 'pygame tornado'
    vim.command('!%s -m pip install %s %s' % (
                pip_bin, mds, trust))
    print('出现错误，请重启vim再加载配置触发安装依赖程序')
    print('安装成功，也请重启使之生效')


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
            "mp3player"])

sys.path.append(pypath)

from threading import Thread
from mp3player_client import Mp3Client

try:
    vim.command('messages clear')
    c = Mp3Client()
    cmd = vim.eval(('input("请输入命令以控制音乐盒子'
                    '[start,stop,next,prev,pause,unpause'
                    ',quit,list,play_index]:")'))
    vim.command('echo "\n"')
    c.send(cmd)
except Exception as e:
    print(e)

EOF

endfunction


nmap <leader>2 :call Self_mp3client_send()<cr>
