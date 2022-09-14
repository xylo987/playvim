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


function! Self_mp3client_send_start()

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
c.send_start()

EOF

endfunction


nmap <leader>2 :call Self_mp3client_send_start()<cr>


function! Self_mp3client_send_stop()

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
c.send_stop()

EOF

endfunction


nmap <leader>3 :call Self_mp3client_send_stop()<cr>


function! Self_mp3client_send_pause()

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
c.send_pause()

EOF

endfunction


nmap <leader>4 :call Self_mp3client_send_pause()<cr>



function! Self_mp3client_send_unpause()

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
c.send_unpause()

EOF

endfunction


nmap <leader>5 :call Self_mp3client_send_unpause()<cr>


function! Self_mp3client_send_next()

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
c.send_next()

EOF

endfunction


nmap <leader>6 :call Self_mp3client_send_next()<cr>


function! Self_mp3client_send_prev()

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
c.send_prev()

EOF

endfunction


nmap <leader>7 :call Self_mp3client_send_prev()<cr>
