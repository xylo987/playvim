import socket
import struct
import json
import traceback


class Client(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sock = socket.socket()

    def get_name(self):
        try:
            return getattr(self, '_name')
        except Exception:
            return None

    def login(self, name):
        try:
            self._sock.connect((self._host, self._port))
            data = json.dumps({
                'action': 'login',
                'name': name
            }).encode()
            send_header = struct.pack('!i', len(data))
            self._sock.send(send_header + data)

            recv_header = self._sock.recv(4)
            data_size, = struct.unpack('!i', recv_header)

            packet = b''
            has_read = 0
            while not getattr(self._sock, '_closed') \
                    and has_read < data_size:
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
            jd = json.loads(packet)
            if jd['status'] == 200:
                self._name = name
                return True
            else:
                self.close()
                return False
        except Exception:
            print(traceback.format_exc())
            return False

    def status(self):
        try:
            return not getattr(self._sock, '_closed')
        except Exception as e:
            print(e)
            return False

    def recv(self):
        if getattr(self, '_name'):
            try:
                recv_header = self._sock.recv(4)
                if len(recv_header) == 0:
                    raise
                data_size, = struct.unpack('!i', recv_header)
                packet = b''
                has_read = 0
                while not getattr(self._sock, '_closed') and\
                        has_read < data_size:
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
                jd = json.loads(packet)
                return jd
            except Exception:
                print(traceback.format_exc(), packet)
                return None
        else:
            raise Exception('您未登陆就想要接收消息显然是错误的')

    def send(self, to, msg, action):
        if getattr(self, '_name'):
            jd = {
                'action': action,
                'from': self._name,
                'to': to,
                'msg': msg
            }
            try:
                jd = json.dumps(jd).encode()
                send_header = struct.pack('!i', len(jd))
                self._sock.send(send_header + jd)
                return True
            except Exception:
                print(traceback.format_exc())
                return False
        else:
            raise Exception('您未登陆就要聊天显然是错误的')

    def qunfa(self, msg):
        if getattr(self, '_name'):
            jd = {
                'action': 'qunfa',
                'from': self._name,
                'msg': msg
            }
            try:
                jd = json.dumps(jd).encode()
                send_header = struct.pack('!i', len(jd))
                self._sock.send(send_header + jd)
                return True
            except Exception:
                print(traceback.format_exc())
                return False
        else:
            raise Exception('您未登陆就要群发显然是错误的')

    def quit(self):
        jd = json.dumps({
            'action': 'quit'
        }).encode()
        send_header = struct.pack('!i', len(jd))
        self._sock.send(send_header + jd)

    def close(self):
        try:
            self._sock.close()
        except Exception:
            print(traceback.format_exc())


if __name__ == '__main__':
    c0 = Client('localhost', 23456)
    c1 = Client('localhost', 23456)
    c2 = Client('localhost', 23456)
    err = 0
    try:
        if c0.login('xh'):
            print('xh登陆成功')
            print('成员:', c0.recv())
        else:
            print('xh登陆失败')
            err = err + 1
        if c1.login('xb'):
            print('xb登陆成功')
            print('成员:', c0.recv())
        else:
            print('xb登陆失败')
            err = err + 1
        if c2.login('xl'):
            print('xl登陆成功')
            print('成员:', c0.recv())
        else:
            print('xl登陆失败')
            err = err + 1

        if err > 0:
            import sys
            sys.exit(-1)
        else:
            print('测试转发')
            if c0.send('xb', '你好xb，我是xh', 'forward'):
                print('1. xh 发送消息 给 xb 成功')
            jd = c1.recv()
            if jd:
                print(jd)
            else:
                print('c1接收数据失败')
            if c1.send('xh', '很高兴收到你的消息', 'forward'):
                print('2. xb 发送消息 给 xh 成功')
            else:
                print('2. xb 发送消息 给xh 失败')
            jd = c0.recv()
            if jd:
                print(jd)
            else:
                print('c0接收数据失败')

            print('测试群发')
            if c2.qunfa('你们哪里啊？'):
                print('c0群消息:', c0.recv())
                print('c1群消息:', c1.recv())
            else:
                print('群发失败')
    except Exception:
        import traceback
        print(traceback.format_exc())
    finally:
        c0.close()
        c1.close()
        c1.close()
