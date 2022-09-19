fun Chat_server()

python3 << EOF    

import sys
import json
import os
import vim

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "chat"])

sys.path.append(pypath)
from server import Server, StatusMemoryFactory
from threading import Thread

s = None
try:
    cfg = os.path.sep.join(
        [vim.eval('expand("$HOME")'), '.vim', '.chat_cfg.json'])
    with open(cfg, 'r') as f:
        jd = json.load(f)
        host = jd['host']
        port = jd['port']
        sf = StatusMemoryFactory()
        sm = sf.get_status_memory('LocalStatusMemory')
        s = Server(host, port, sm)
        t = Thread(target=s.start, daeon=True)
        t.start()
except Exception:
    if s: s.close()
finally:
    print('聊天服务器已启动')

EOF

endfun


fun Chat_start()

python3 << EOF

import sys
import json
import os
import vim

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "chat"])

sys.path.append(pypath)
from ui import App
from threading import Thread

try:
    cfg = os.path.sep.join(
        [vim.eval('expand("$HOME")'), '.vim', '.chat_cfg.json'])
    with open(cfg, 'r') as f:
        jd = json.load(f)
        host = jd['host']
        port = jd['port']
        name = jd['name']
        cmd = 'python3 %s/%s' % (pypath, 
                'ui.py %s %s %s' % (host, port, name))
        Thread(target=os.system, args=(cmd,), daemon=True).start()
except Exception: pass

EOF

endfun


fun Chat_config_server()

python3 << EOF

import sys
import json
import os
import vim

try:
    cfg = os.path.sep.join([
                    vim.eval('expand("$HOME")'), '.vim', '.chat_cfg.json'])
    host = vim.eval('input("请输入服务器地址:")')
    port = int(vim.eval('input("请输入服务器端口:")'))
    name = vim.eval('input("请输入您的名字:")')
    with open(cfg, 'w') as f:
        json.dump({
            'host': host,
            'port': port,
            'name': name
        }, f)
    print('配置成功')
except KeyboardInterrupt:
    print('用户已取消该操作')
    
EOF

endfun


nmap <leader>4 :call Chat_config_server()<CR>
nmap <leader>5 :call Chat_server()<CR>
nmap <leader>6 :call Chat_start()<CR>
