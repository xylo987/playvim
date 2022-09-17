import socket
import json
from threading import Thread, Lock


class StatusMemory(object):
    def __init__(self):
        self._cm = dict()
        self._lock = Lock()

    def set(self, name, connect):
        with self._lock:
            self._cm[name] = connect

    def get(self, name):
        try:
            return self._cm[name]
        except Exception:
            return None

    def remove(self, name):
        with self._lock:
            del self._cm[name]

    def all(self):
        return self._cm


class Handle(object):
    def __init__(self, connect, status_memory):
        self._connect = connect
        self._status_memory = status_memory

    def _login(self):
        """
        握手，建立连接
        """
        try:
            while getattr(self._connect, '_closed'):
                packet = b''
                while 1 < 2:
                    d = self._connect.read(1024)
                    if len(d) > 0:
                        packet = packet + d

                packet_json = json.loads(packet.decode())
                name = packet_json['name']

                if self._status_memory.get(name):
                    self._connect.write(json.dumps({
                        'status': 404,
                        'msg': '该名字已经登陆'
                    }))
                    return None
                else:
                    self._connect.write(json.dumps({
                        'status': 200,
                        'msg': '登陆成功'
                    }))
                    self._status_memory.set(name, self._connect)
                    return name
        except Exception:
            self._close()
            return None

    def forward(self):
        """
        转发消息之前，需要先登陆，否则就直接退出
        转发消息，消息的数据结构
        {
            'form': '小红',
            'to': '小黑',
            'msg': '你好',
            'sj': '2020-09-17 21:17:20'
        }
        """
        name = self._login()
        if name:
            try:
                while getattr(self._connect, '_closed'):
                    packet = b''
                    while 1 < 2:
                        d = self._connect.read(1024)
                        if len(d) > 0:
                            packet = packet + d
                        break
                    packet_json = json.loads(packet.decode())
                    packet_json['from'] = self._name
                    to = packet_json['to']
                    remote_conn = self._status_memory.get(to)
                    remote_conn.write(packet)
            except Exception:
                self.close()

    def _close(self):
        try:
            self._connect.close()
            self._status_memory.remove(self._name)
        except Exception as e:
            print(e)


class Server(object):
    def __init__(self, port):
        self._port = port
        self._status_memory = StatusMemory()

    def start(self):
        s = socket.socket()
        self._sock = s
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))

        s.listen(5)

        while True:
            if not getattr(s, '_closed'):
                c, addr = s.accept()
                handle = Handle(c, self._status_memory)
                t = Thread(target=handle.forward)
                t.start()

    def close(self):
        for name, conn in self._status_memory.all():
            try:
                conn.close()
                self._status_memory.remove(name)
            except Exception:
                pass
