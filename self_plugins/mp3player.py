"""
mp3播放器的业务逻辑程序

用到pygame库，下面是一些与播放音乐有关的函数:

    pygame.mixer.music.load()           ——  载入一个音乐文件用于播放
    pygame.mixer.music.play()           ——  开始播放音乐流
    pygame.mixer.music.rewind()         ——  重新开始播放音乐
    pygame.mixer.music.stop()           ——  结束音乐播放
    pygame.mixer.music.pause()          ——  暂停音乐播放
    pygame.mixer.music.unpause()        ——  恢复音乐播放
    pygame.mixer.music.fadeout()        ——  淡出的效果结束音乐播放
    pygame.mixer.music.set_volume()     ——  设置音量
    pygame.mixer.music.get_volume()     ——  获取音量
    pygame.mixer.music.get_busy()       ——  检查是否正在播放音乐
    pygame.mixer.music.set_pos()        ——  设置播放的位置
    pygame.mixer.music.get_pos()        ——  获取播放的位置
    pygame.mixer.music.queue()          ——  将一个音乐文件放入队列中，并排在当
                                            前播放的音乐之后
    pygame.mixer.music.set_endevent()   ——  当播放结束时发出一个事件
    pygame.mixer.music.get_endevent()   ——  获取播放结束时发送的事件


问题

    不同的平台的音频解码有一些不同，比如safari和charome，safari能播放的mp3，
    chrome 就不能播放，针对一些特别的mp3文件


下面是实现代码
"""


from abc import abstractmethod, ABCMeta
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'yes'
from pygame.mixer import music
from pygame import init, quit


class MP3PlayerInterface(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def update_status(self):
        raise NotImplementedError()

    @abstractmethod
    def open(self):
        raise NotImplementedError()

    @abstractmethod
    def quit(self):
        raise NotImplementedError()

    @abstractmethod
    def play(self, audio_interface):
        raise NotImplementedError()

    @abstractmethod
    def get_pos(self):
        raise NotADirectoryError()

    @abstractmethod
    def pause(self):
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        raise NotImplementedError()

    @abstractmethod
    def unpause(self):
        raise NotADirectoryError()

    @abstractmethod
    def append_play_list(self, audio_interface):
        raise NotImplementedError()

    @abstractmethod
    def next(self):
        raise NotImplementedError()

    @abstractmethod
    def prev(self):
        raise NotImplementedError()

    @abstractmethod
    def get_len_musics(self):
        raise NotImplementedError()

    @abstractmethod
    def get_title(self):
        raise NotImplementedError()


class TypeOneAudioInterface(metaclass=ABCMeta):
    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def load_typeone(self):
        raise NotImplementedError()

    @abstractmethod
    def play_typeone(self):
        raise NotImplementedError()

    @abstractmethod
    def get_pos_typeone(self):
        raise NotADirectoryError()

    @abstractmethod
    def pause_typeone(self):
        raise NotImplementedError()

    @abstractmethod
    def stop_typeone(self):
        raise NotImplementedError()

    @abstractmethod
    def unpause_typeone(self):
        raise NotADirectoryError()

    @abstractmethod
    def get_title(self):
        raise NotADirectoryError()

    @abstractmethod
    def unload_typeone(self):
        raise NotImplementedError()

    @abstractmethod
    def get_buzy_typeone(self):
        raise NotImplementedError()


class TypeOneMp3AudioAdapter(TypeOneAudioInterface):
    def __init__(self, filename, title):
        self._filename = filename
        self._title = title

    def get_buzy_typeone(self):
        return music.get_buzy()

    def get_title(self):
        return self._title

    def load_typeone(self):
        music.load(self._filename)

    def unload_typeone(self):
        music.unload()

    def close(self):
        pass

    def play_typeone(self):
        music.play()

    def get_pos_typeone(self):
        return music.get_pos()

    def pause_typeone(self):
        music.pause()

    def stop_typeone(self):
        music.stop()
        self.unload_typeone()

    def unpause_typeone(self):
        music.unpause()


class Mp3Player(MP3PlayerInterface):
    def __init__(self):
        self._play_list = list()
        self._playing_count = None
        # playing, pause, stop, quit
        self._status = 'stop'

    def get_status(self): 
        return self._status

    def open(self):
        init() 

    def quit(self):
        self.stop()
        for ai in self._play_list:
            ai.close()
        self._play_list.clear()
        self._status = 'quit'
        self._playing_count = None
        quit()

    def play(self, audio_interface):
        self.append_play_list(audio_interface)

        if isinstance(audio_interface, TypeOneMp3AudioAdapter):
            if self._status not in ['playing', 'pause']:
                audio_interface.load_typeone()

            if self._playing_count is None:
                self._playing_count = 0

            self._status = 'playing'
            audio_interface.play_typeone()

    def get_pos(self):
        if self._status not in ['stop', 'quit']:
            audio_interface = self._play_list[self._playing_count]
            sec = audio_interface.get_pos_typeone()
            return sec

    def pause(self):
        if self._status == 'playing':
            audio_interface = self._play_list[self._playing_count]
            audio_interface.pause_typeone()
            self._status = 'pause'

    def stop(self):
        if self._status in ['playing', 'pause']:
            audio_interface = self._play_list[self._playing_count]
            audio_interface.stop_typeone()

        self._status = 'stop'

    def unpause(self):
        if self._status == 'pause':
            audio_interface = self._play_list[self._playing_count]
            audio_interface.unpause_typeone()
            self._status = 'playing'

    def append_play_list(self, audio_interface):
        if audio_interface not in self._play_list and \
                isinstance(audio_interface, (TypeOneAudioInterface, )):
            self._play_list.append(audio_interface)
            if self._playing_count is None:
                self._playing_count = 0

    def next(self):
        self.stop()
        if 0 <= self._playing_count < len(self._play_list) - 1:
            self._playing_count = self._playing_count + 1
        else:
            self._playing_count = 0

        audio_interface = self._play_list[self._playing_count]
        self.play(audio_interface)

    def start(self):
        l = self.get_len_musics()
        if l > 0:
            self._playing_count = l - 1
            audio_interface = self._play_list[self._playing_count]
            self.play(audio_interface)

    def prev(self):
        self.stop()
        if 0 < self._playing_count <= len(self._play_list):
            self._playing_count = self._playing_count - 1
        else:
            self._playing_count = len(self._play_list) - 1

        audio_interface = self._play_list[self._playing_count]
        self.play(audio_interface)

    def update_status(self):
        if self._playing_count is not None:
            audio_interface = self._play_list[self._playing_count]
            pos = audio_interface.get_pos_typeone()
            if pos == -1:
                audio_interface.unload_typeone()
                self._status = 'stop'

    def get_len_musics(self):
        return len(self._play_list)

    def get_title(self):
        if self._playing_count is not None:
            if 0 <= self._playing_count < len(self._play_list):
                audio_interface = self._play_list[self._playing_count]
                return audio_interface.get_title()
        return None



def loop():
    import time
    import os
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
                print(str(e))

    m.start()

    while m.get_status() != 'quit':
        m.update_status()
        if m.get_status() == 'stop':
            m.next()
        time.sleep(5)



def main():
    #  仅仅在主进程中可用
    import signal
    import os

    class InputTimeoutError(Exception):
        pass

    def interrupted(signum, frame):
        raise InputTimeoutError

    signal.signal(signal.SIGALRM, interrupted)

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

    m.start()
    print('\n|万万音乐> [%s] --- %s ---%d(s)|' % ( 
            m.get_status(), 
            m.get_title() or '',
            (m.get_pos() or 0) / 1000))
    while m.get_status() not in ['quit']:
        try:
            m.update_status()
            signal.alarm(5)

            prompt = input('请输入口令[quit, pause, unpause, next, prev, stop, start]:')
            if prompt == 'quit':
                m.quit()
                break
            elif prompt == 'pause':
                m.pause()
            elif prompt == 'unpause':
                m.unpause()
            elif prompt == 'next':
                m.next()
            elif prompt == 'stop`':
                m.stop()
            elif prompt == 'prev':
                m.prev()
            else:
                print('不支持的选项')
        except InputTimeoutError:
            print('\n|万万音乐> [%s] --- %s ---%d(s)|' % ( 
                m.get_status(), 
                m.get_title() or '',
                (m.get_pos() or 0) / 1000))


if __name__ == '__main__':
    main()
