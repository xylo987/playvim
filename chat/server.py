import socket
import struct
import json
from threading import Thread, Lock
from abc import ABCMeta, abstractmethod

DEBUG = False

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
    提供转发，群发，登陆，退出命令
    当有新用户或者下线，则通知所有在线用户
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
                has_read = 0
                while has_read < data_size:
                    d = b''
                    if data_size - has_read < 1024:
                        d = self._sock.recv(data_size - has_read)
                    else:
                        d = self._sock.recv(1024)
                    ld = len(d)
                    if ld > 0:
                        has_read = has_read + ld
                        packet = packet + d
                    else:
                        break
                try:
                    packet_json = json.loads(packet.decode())
                    self._deal(packet_json, packet)
                except Exception:
                    self._error()
        except Exception as e:
            if DEBUG:
                import traceback
                print(traceback.format_exc())
            else: print(e)
        finally:
            self._close()
            self._clear_status_memory()

    def _error(self):
        jd = json.dumps({
            'status': 500,
            'msg': '数据格式错误'
        }).encode()
        send_header = struct.pack('!i', len(jd))
        self._sock.send(send_header + jd)

    def _deal(self, packet_json, packet):
        cmd = packet_json['action']
        if cmd == 'login':
            # {'action': 'login', 'name': xx}
            self._login(packet_json)
            self._notify_all()
        elif cmd == 'qunfa':
            # {'action': 'qunfa', 'from': xx, 'msg': xx}
            self._send_all(packet)
        elif cmd == 'forward':
            # {'action': 'forward', 'from': xx, 'to': xx, 'msg': xx}
            self._forward(packet_json, packet)
        elif cmd == 'quit':
            # {'action': 'quit', 'name': xx}
            self._quit()
            self._notify_all()
        else:
            self._error()

    def _send_all(self, packet):
        for conn in list(self._status_memory.all().values()):
            if conn != self._sock:
                self._send_one(conn, packet)

    def _send_one(self, conn, packet):
        send_header = struct.pack('!i', len(packet))
        conn.send(send_header + packet)

    def _notify_one(self, names, conn):
        jd = json.dumps({
            'action': 'notify',
            'names': names
        }).encode()
        send_header = struct.pack('!i', len(jd))
        conn.send(send_header + jd)

    def _notify_all(self):
        names = list(self._status_memory.all().keys())
        conns = list(self._status_memory.all().values())
        for conn in conns:
            self._notify_one(names, conn)

    def _quit(self):
        self._close()
        self._clear_status_memory()

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
        """
        { 'from: xx, 'to': xx, ...}
        """
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

    def _close(self):
        try:
            self._sock.close()
        except Exception as e:
            print(e)

    def _clear_status_memory(self):
        try:
            self._status_memory.remove(self._name)
        except Exception:
            pass


class Server(object):
    def __init__(self, host, port, status_memory):
        self._host = host
        self._port = port
        self._status_memory = status_memory

    def start(self):
        try:
            s = socket.socket()
            self._sock = s
            s.bind((self._host, self._port))

            s.listen(5)
            while not getattr(s, '_closed'):
                try:
                    c, addr = s.accept()
                    handle = Handle(c, self._status_memory)
                    t = Thread(target=handle.handle)
                    t.start()
                except Exception as e:
                    print(e)
        except Exception as e:
            if DEBUG:
                import traceback
                print(traceback.format_exc())
            else:
                print(e)
        finally:
            if getattr(self, 'close'):
                self.close()

    def close(self):
        for name, conn in self._status_memory.all():
            try:
                conn.close()
            except Exception:
                pass
            try:
                self._status_memory.remove(name)
            except Exception:
                pass


if __name__ == '__main__':
    try:
        sf = StatusMemoryFactory()
        sm = sf.get_status_memory('LocalStatusMemory')
        s = Server('localhost', 23456, sm)
        s.start()
    finally:
        s.close()
