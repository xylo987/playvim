import socket
import struct
import json
from threading import Thread, Lock
from abc import ABCMeta, abstractmethod


class StatusMemoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def set(self, name, conn):
        raise NotImplementedError()

    @abstractmethod
    def get(self, name):
        raise NotImplementedError()

    @abstractmethod
    def remove(self, name):
        raise NotImplementedError()

    @abstractmethod
    def all(self):
        raise NotImplementedError()


class LocalStatusMemory(StatusMemoryInterface):
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


class StatusMemoryFactory(object):
    def get_status_memory(self, status_memory):
        if status_memory == 'LocalStatusMemory':
            return LocalStatusMemory()
        else:
            return None


class Handle(object):
    """
    提供转发，登陆，退出命令
    """
    def __init__(self, connect, status_memory):
        self._sock = connect
        self._status_memory = status_memory

    def handle(self):
        try:
            while not getattr(self._sock, '_closed'):
                recv_header = self._sock.recv(4)
                if len(recv_header) == 0:
                    break
                data_size, = struct.unpack('!i', recv_header)
                packet = b''
                while len(packet) < data_size:
                    d = self._sock.recv(1024)
                    if len(d) > 0:
                        packet = packet + d
                    else:
                        break
                try:
                    packet_json = json.loads(packet.decode())
                    self._deal(packet_json, packet)
                except Exception:
                    self._error()
        except Exception:
            import traceback
            print(traceback.format_exc())
        finally:
            self._close()

    def _error(self):
        jd = json.dumps({
            'status': 500,
            'msg': '数据格式错误'
        }).encode()
        send_header = struct.pack('!i', len(jd))
        self._sock.send(send_header + jd)

    def _deal(self, packet_json, packet):
        try:
            cmd = packet_json['action']
            if cmd == 'login':
                self._login(packet_json)
            elif cmd == 'forward':
                self._forward(packet_json, packet)
            elif cmd == 'quit':
                self._quit()
            else:
                self._error()
        except Exception:
            self._error()

    def _quit(self):
        self._close()

    def _login(self, packet_json):
        name = packet_json['name']
        if self._status_memory.get(name):
            jd = json.dumps({
                'status': 404,
                'msg': '该名字已经登陆'
            }).encode()
            send_header = struct.pack('!i', jd)
            self._sock.send(send_header + jd)
            self._close_for_login()
        else:
            self._name = name
            self._status_memory.set(name, self._sock)
            jd = json.dumps({
                'status': 200,
                'msg': '登陆成功，您现在就是%s了' % name
            }).encode()
            send_header = struct.pack('!i', len(jd))
            self._sock.send(send_header + jd)

    def _forward(self, packet_json, packet):
        to = packet_json['to']
        remote_conn = self._status_memory.get(to)
        if remote_conn:
            send_header = struct.pack('!i', len(packet))
            remote_conn.send(send_header + packet)
        else:
            jd = json.dumps({
                'status': 404,
                'msg': '目标用户不在线'
            }).encode()
            send_header = struct.pack('!i', len(jd))
            self._sock.send(send_header + jd)

    def _close_for_login(self):
        try:
            self._sock.close()
        except Exception as e:
            print(e)

    def _close(self):
        try:
            self._sock.close()
            self._status_memory.remove(self._name)
        except Exception as e:
            print(e)


class Server(object):
    def __init__(self, port, status_memory):
        self._port = port
        self._status_memory = status_memory

    def start(self):
        s = socket.socket()
        self._sock = s
        s.bind(('0.0.0.0', self._port))

        s.listen(5)

        while not getattr(s, '_closed'):
            try:
                c, addr = s.accept()
                handle = Handle(c, self._status_memory)
                t = Thread(target=handle.handle)
                t.start()
            except Exception as e:
                print(e)

        self.close()

    def close(self):
        for name, conn in self._status_memory.all():
            try:
                conn.close()
                self._status_memory.remove(name)
            except Exception:
                pass


if __name__ == '__main__':
    try:
        sf = StatusMemoryFactory()
        sm = sf.get_status_memory('LocalStatusMemory')
        s = Server(23456, sm)
        s.start()
    finally:
        s.close()
