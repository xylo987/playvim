function! Self_plugins_StartMp3Player()

python3 << EOF

import sys
import os
import vim

pypath = os.path.sep.join([vim.eval("expand('$HOME')"), ".vim_runtime",
            "self_plugins"])

sys.path.append(pypath)

from threading import Thread
from mp3player import loop

t = Thread(target=loop, daemon=True)
t.start()

EOF

endfunction


nmap <F4> :call Self_plugins_StartMp3Player()<cr>
