import socket


class Mp3Client(object):
    def __init__(self):
        self._host = 'localhost'
        self._port = 12345

        self._sock = socket.socket()
        self._sock.connect((self._host, self._port))

    def _send(self, cmd):
        try:
            print("client:", cmd)
            self._sock.send(cmd.encode())
        except Exception as e:
            print(e)
        finally:
            self._sock.close()

    def send_start(self):
        self._send('start')

    def send_stop(self):
        self._send('stop')

    def send_pause(self):
        self._send('pause')

    def send_unpause(self):
        self._send('unpause')

    def send_next(self):
        self._send('next')

    def send_prev(self):
        self._send('prev')


if __name__ == '__main__':
    c = Mp3Client()
    #c.send_start()
    c.send_next()
