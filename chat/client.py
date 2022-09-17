import socket
import json


class Client(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sock = socket.socket()

    def login(self, name):
        self._name = name
        try:
            self._sock.connect((self._host, self._port))
            self._sock.send(json.dumps({
                'name': name
            }))
            packet = b''
            while getattr(self._sock, '_closed'):
                d = self._sock.recv(1024)
                if len(d) > 0:
                    packet = packet + d
                else:
                    break
            jd = json.loads(packet)
            if jd['status'] == 200:
                self._name = name
                return True
        except Exception as e:
            print(e)
            return False

    def recv(self):
        try:
            packet = b''
            while getattr(self._sock, '_closed'):
                d = self._sock.recv(1024)
                if len(d) > 0:
                    packet = packet + d
                else:
                    break
            jd = json.loads(packet)
            return jd
        except Exception as e:
            print(e)
            return None

    def send(self, to, msg):
        jd = {
            'from': self._name,
            'to': to,
            'msg': msg
        }
        try:
            self._sock.send(json.dumps(jd))
            return True
        except Exception as e:
            print(e)
            return False

    def close(self):
        try:
            self._sock.close()
        except Exception as e:
            print(e)
