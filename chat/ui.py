import sys
import tkinter
import tkinter.messagebox
from client import Client
from threading import Thread, Timer


class App(object):
    def __init__(self, debug=False):
        self._debug = debug
        self._root = tkinter.Tk()
        self._root.title('Chat')
        self._root.resizable(width=0, height=0)
        sw = self._root.winfo_screenwidth()
        sh = self._root.winfo_screenheight()
        ww = 768
        wh = 600
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self._root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

    def msg_div(self):
        div = tkinter.LabelFrame(self._root)

        l = tkinter.Label(div, text='聊天信息')
        l.configure(background='black')
        l.configure(foreground='white')
        '''
        anchor表示文字或图片的对齐方式
        nw        n         ne
        w       center       e
        sw        s         se
        '''
        l.configure(anchor='center')
        l.pack(fill=tkinter.X, side=tkinter.TOP)

        sb = tkinter.Scrollbar(div)
        sb.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        t = tkinter.Text(div, yscrollcommand=sb.set)
        #t.configure(state='disabled')
        t.configure(background='white')
        t.configure(foreground='green')

        t.pack(fill=tkinter.BOTH, expand=True)
        div.place(x=0, y=0, width=600, height=400)
        self._msg = t

    def chat_div(self):
        div = tkinter.LabelFrame(self._root)
        l = tkinter.Label(div, text='信息输入')
        l.configure(background='black')
        l.configure(foreground='white')
        l.place(x=0, y=0, width=600, height=20)

        sb = tkinter.Scrollbar(div)
        sb.place(x=480, y=20, width=20, height=200)
        t = tkinter.Text(div, yscrollcommand=sb.set)
        t.configure(background='white')
        t.configure(foreground='green')
        t.place(x=0, y=20, width=580, height=170)

        b = tkinter.Button(div, text='发送', bg='blue', fg='green',
                           command=self.send_msg)
        b.place(x=0, y=170, width=600, height=30)

        div.place(x=0, y=400, width=600, height=200)
        self._chat = t

    def users_div(self):
        div = tkinter.LabelFrame(self._root)
        l = tkinter.Label(div, text='成员')
        l.configure(background='black')
        l.configure(foreground='white')
        l.place(x=0, y=0, width=168, height=20)

        sb = tkinter.Scrollbar(div)
        sb.place(x=148, y=20, width=20, height=580)
        ul = tkinter.Listbox(div, yscrollcommand=sb.set)
        ul.place(x=0, y=20, width=148, height=580)
        self._ul = ul

        div.place(x=600, y=0, width=268, height=600)

    def add_user(self, name):
        self._ul.insert('end', name)

    def del_user(self, name):
        for i in range(self._ul.size()):
            if self._ul.get(i) == name:
                self._ul.delete(i)
                break

    def update_users(self, names):
        self._ul.delete(0, last=self._ul.size() - 1)
        for name in names:
            self.add_user(name)

    def recv_msg(self):
        while self._cli.status():
            jd = self._cli.recv()
            if not jd:
                if self._debug:
                    tkinter.messagebox.showinfo('信息提示框', '客户端已断开')
                sys.exit(-1)
            if self._debug:
                tkinter.messagebox.showinfo('调试', str(jd))
            if jd['action'] == 'qunfa':
                fr = jd['from']
                msg = jd['msg']
                self.append(fr, msg)
            elif jd['action'] == 'notify':
                self.update_users(jd['names'])
            else:
                if self._debug:
                    tkinter.messagebox.showinfo('消息提示框', '其它命令还未支持')

    def send_msg(self):
        if self._cli.status():
            msg = self._chat.get('1.0', 'end')
            if self._debug:
                tkinter.messagebox.showinfo('调试信息', msg)
            fr = self._cli.get_name()
            self.append(fr, msg)
            if self._cli.qunfa(msg):
                self._chat.delete('1.0', 'end')

    def login(self, host, port, name):
        self._cli = Client(host, port)
        if not self._cli.login(name):
            if self._debug:
                tkinter.messagebox.showinfo(
                '消息提示框', '登陆失败, 用户名已存在或服务器未启动')
            return False
        return True

    def append(self, fr, msg):
        data = '%s:\n\t%s\n' % (fr, msg)
        if self._debug:
            tkinter.messagebox.showinfo('调试信息', data)
        self._msg.insert('end', data)

    def show(self):
        self.msg_div()
        self.chat_div()
        self.users_div()
        t = Thread(target=self.recv_msg, daemon=True)
        ti = Timer(5, t.start)
        ti.start()
        self._root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self._root.mainloop()

    def on_closing(self):
        self._cli.quit()
        sys.exit(-1)


if __name__ == '__main__':
    import sys

    app = App()
    if app.login(sys.argv[1], int(sys.argv[2]), sys.argv[3]):
        app.show()
