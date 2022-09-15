import os
import socket
from mp3player import Mp3Player, TypeOneMp3AudioAdapter


class Mp3Server(object):
    def __init__(self):
        m = Mp3Player()
        m.open()
        path = os.path.sep.join([os.path.dirname(__file__), 'mp3s'])

        for file in os.listdir(path):
            if file.endswith('.mp3'):
                try:
                    adp = TypeOneMp3AudioAdapter(os.path.sep.join([path, file]), 
                            file.rsplit('.')[0])
                    m.append_play_list(adp)
                except Exception as e:
                    pass
        self._m = m

    def main(self):
        s = socket.socket()
        self._sock = s
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))

        s.listen(5)

        while True:
            if not getattr(s, '_closed'):
                c,addr = s.accept()
                if self.handle(c):
                    s.close()

    def handle(self, c):
        err = False
        try:
            cmd = c.recv(1024).decode()
            if cmd == 'start':
                self._m.start()
            elif cmd == 'stop':
                self._m.stop()
            elif cmd == 'pause':
                self._m.pause()
            elif cmd == 'unpause':
                self._m.unpause()
            elif cmd == 'next':
                self._m.next()
            elif cmd == 'prev':
                self._m.prev()
            elif cmd == 'quit':
                self._m.quit()
                err = True
            else:
                print(('命令不支持,可支持的命令为:'
                       '[start,stop,pause,unpause,next,prev,quit]'))
        except Exception as e:
            print(e)
        finally:
            try:
                c.close()
            except Exception as e:
                print(e)
            return err


if __name__ == '__main__':
    s = Mp3Server()
    s.main()
