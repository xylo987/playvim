import os
import json
import asyncio
import socket
import tornado.web


def send_updated():
    s = None
    try:
        s = socket.socket()
        s.connect(('localhost', 12345))
        s.send('updated'.encode())
        s.recv(1024)
    except Exception:
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass


class BaseHandler(tornado.web.RequestHandler):
    music_path = os.path.sep.join([os.path.dirname(__file__), 'mp3s'])

    @classmethod
    def load_all_mp3(self):
        all_mp3 = []
        i = 0
        for file in os.listdir(BaseHandler.music_path):
            if file.endswith('.mp3'):
                fp = os.path.sep.join([BaseHandler.music_path, file])
                fn = file.rsplit('.')[0]
                all_mp3.append((i, fn, fp))
                i = i + 1
        return all_mp3

    def get(self):
        self.render('index.html')

    def post(self):
        # page = int(self.get_argument('page'))
        all_mp3 = self.load_all_mp3()

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps({
            'status': 200,
            'data': all_mp3
        }))


class DelHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            index = int(self.get_argument('index'))
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            _, _, fp = BaseHandler.load_all_mp3()[index]
            os.remove(fp)
            send_updated()
            self.write(json.dumps({'status': 200}))
        except Exception:
            self.write(json.dumps({'status': 404}))


class ReNameHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            index = int(self.get_argument('index'))
            new_name = self.get_argument('new_name')
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            _, _, fp = BaseHandler.load_all_mp3()[index]
            np = os.path.sep.join([BaseHandler.music_path, new_name + '.mp3'])
            if not os.path.exists(np):
                os.rename(fp, np)
            else:
                raise
            send_updated()
            self.write(json.dumps({'status': 200}))
        except Exception:
            self.write(json.dumps({'status': 404}))


class PlayHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            index = int(self.get_argument('index'))
            _, _, fp = BaseHandler.load_all_mp3()[index]
            self.set_header('Content-Type', 'audio/mp3')
            self.set_header('Accept-Ranges', 'bytes')
            with open(fp, 'rb') as f:
                while 1:
                    d = f.read(2048)
                    if not d:
                        break
                    #self.set_header('content-length', len(d)))
                    self.write(d)
        except Exception:
            import traceback
            print(traceback.format_exc())
            self.write(json.dumps({'status': 404}))


class UploadHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        try:
            fs = self.request.files.get('fs')
            fail_fs = []
            for meta in fs:
                fn = None
                try:
                    fn = meta['filename']
                    fb = meta['body']
                    fp = os.path.sep.join([BaseHandler.music_path, fn])
                    if os.path.exists(fp):
                        raise
                    with open(fp, 'wb') as f:
                        f.write(fb)
                except Exception:
                    fail_fs.append(fn)

            if 0 < len(fail_fs) < len(fail_fs):
                send_updated()
                self.write(json.dumps({ 'status': 199, 'data': fail_fs}))
            elif len(fail_fs) == len(fs):
                self.write(json.dumps({ 'status': 198, 'data': fail_fs}))
            else:
                send_updated()
                self.write(json.dumps({ 'status': 200 }))
        except Exception:
            # bug self.redirect(self.reverse_url('index'), status=301)
            self.write(json.dumps({ 'status': 404 }))


def make_app():
    return tornado.web.Application([
            tornado.web.url(r"/", BaseHandler, name='index'),
            (r"/del", DelHandler),
            (r"/rename", ReNameHandler),
            (r"/play", PlayHandler),
            (r"/upload", UploadHandler),
        ],
        template_path=os.path.dirname(__file__),
        static_path=os.path.dirname(__file__),
        debug=True
    )


async def main():
    app = make_app()
    app.listen(12346)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
