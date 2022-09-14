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
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))

        s.listen(5)

        while True:
            c,addr = s.accept()
            self.handle(c)

    def handle(self, c):
        try:
            cmd = c.recv(1024).decode()
            print("server:", cmd)
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
            else:
                print('命令不支持')
        except Exception as e:
            print(e)
        finally:
            c.close()


if __name__ == '__main__':
    s = Mp3Server()
    s.main()
