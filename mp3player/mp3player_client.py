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
            map_cmd = {
                'start': '开始播放',
                'stop': '停止播放',
                'pause': '暂停播放',
                'unpause': '恢复播放',
                'list': '查看歌单',
                'quit': '关闭音乐盒子',
                'next': '下一曲',
                'prev': '上一曲',
                'play_index': '播放指定音乐'
            }
            if not cmd.startswith('play_index'):
                print('我：\n    %s' %  map_cmd[cmd])
            else:
                print('我：\n    %s' %  map_cmd['play_index'] + ' ' + cmd[11:])
            self._sock.send(cmd.encode())
            msg = self._sock.recv(1024)
            if len(msg) != 0:
                print('音乐盒子: %s\n' %  msg.decode())
        except Exception as e:
            print(e)
        finally:
            try:
                self._sock.close()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    c = Mp3Client()
    c.send('start')
