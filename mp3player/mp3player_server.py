import os
import socket
from mp3player import Mp3Player, TypeOneMp3AudioAdapter


class Mp3Server(object):
    def __init__(self):
        self._load()

    def _load(self):
        m = Mp3Player()
        m.open()

        path = os.path.sep.join([os.path.dirname(__file__), 'mp3s'])

        for file in os.listdir(path):
            if file.endswith('.mp3'):
                try:
                    fp = os.path.sep.join([path, file])
                    fn = file.rsplit('.')[0]
                    adp = TypeOneMp3AudioAdapter(fp, fn)
                    m.append_play_list(adp)
                except Exception:
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
                c, addr = s.accept()
                if self.handle(c):
                    s.close()

    def handle(self, c):
        quit = False
        sended = False
        try:
            cmd = c.recv(1024).decode()
            if len(cmd) == 0:
                return
            if cmd == 'updated':
                self._m.quit()
                self._load()
            elif cmd == 'start':
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
                quit = True
            elif cmd == 'list':
                music_list = self._m.get_music_list()
                msg = ''
                for mu in music_list:
                    msg = msg + ('\n    %d. %s\n' % (mu[0] + 1, mu[1]))
                c.send(msg.encode())
                sended = True
            elif cmd.startswith('play_index'):
                try:
                    index = int(int(cmd[11:]))
                    if 0 < index <= self._m.get_len_musics():
                        self._m.play_index(index - 1)
                    else:
                        c.send('\n    请输入正确的音乐的索引'.encode())
                except Exception:
                    c.send('\n    请输入正确的音乐的索引'.encode())
            else:
                c.send(('\n    命令不支持,可支持的命令为:'
                        '[start,stop,pause,unpause,next'
                        ',prev,quit,list,quit, play_index]').encode())
        except Exception:
            import traceback
            print(traceback.format_exc())
        finally:
            return self._fiy(sended, quit, c)

    def _fiy(self, sended, quit, c):
        if not sended and not quit:
            map_status = {
                'playing': '正在播放',
                'pause': '已经暂停',
                'stop': '已经停止',
            }
            title = self._m.get_title()
            pos = self._m.get_pos() or 0
            status = self._m.get_status()
            smsg = '\n    %s--%s--%s' % (
                    map_status[status], title, str(pos / 1000))
            c.send(smsg.encode())
        try:
            c.close()
        except Exception as e:
            print(e)
        return quit


if __name__ == '__main__':
    s = Mp3Server()
    s.main()
