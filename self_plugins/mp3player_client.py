import socket


class Mp3Client(object):
    def __init__(self):
        self._host = 'localhost'
        self._port = 12345

        try:
            self._sock = socket.socket()
            self._sock.connect((self._host, self._port))
        except Exception:
            print('请输入<leader>1启动音乐盒子服务器')

    def send(self, cmd):
        try:
            self._sock.send(cmd.encode())
        except Exception as e:
            print(e)
        finally:
            try:
                self._sock.close()
            except Exception as e:
                print(e)

    def send_start(self):
        self.send('start')

    def send_stop(self):
        self.send('stop')

    def send_pause(self):
        self.send('pause')

    def send_unpause(self):
        self.send('unpause')

    def send_next(self):
        self.send('next')

    def send_prev(self):
        self.send('prev')


if __name__ == '__main__':
    c = Mp3Client()
    #c.send_start()
    c.send_next()
