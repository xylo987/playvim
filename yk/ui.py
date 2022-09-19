import tkinter
from tkinter import ttk


class App(object):
    def __init__(self):
        self.html()

    def html(self):
        self._body = tkinter.Tk(className='远控')
        self._body.configure(background='gray')

        sw = self._body.winfo_screenwidth()
        sh = self._body.winfo_screenheight()
        ww = 768
        wh = 600
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self._body.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

        pingmu_div = self.pingmu_div(self._body)
        term_div = self.term_div(self._body)
        target_div = self.target_div(self._body)

        pingmu_div.configure(
            borderwidth=3, relief='sunken', background='red')
        pingmu_div.pack(
            fill=tkinter.BOTH, side=tkinter.TOP, expand=True,
            padx=5, pady=5)

        term_div.configure(
            borderwidth=3, relief='sunken', background='blue')
        term_div.pack(
            fill=tkinter.X, side=tkinter.BOTTOM,
            padx=5, pady=5)

        target_div.configure(
            borderwidth=3, relief='sunken', background='yellow')
        target_div.pack(
            fill=tkinter.X, side=tkinter.RIGHT,
            padx=5, pady=5)

    def pingmu_div(self, master):
        # NOTE. 凉了，比如说我这个屏幕div里要播放N个远控的屏幕Video标签
        # 这时候就做不了，因为tkinter里只有text和listbox支持scrollbar
        # 这不是凉了吗？
        pw = tkinter.PanedWindow(master)
        return pw

    def term_div(self, master):
        # 再比如，我要在终端选项卡里做一个可以切换终端的终端又scroll，当然可以
        # 借助text自带的东西实现，但是一看这不是个简单的事情
        pw = tkinter.PanedWindow(master)
        return pw

    def target_div(self, master):
        # 这个同上，这个简直无法做。
        # 借用 知乎https://www.zhihu.com/question/32703639的回答，这些坑
        # 我基本遇到了一些，但是想让我去玩pyqt那是绝对不可能的，老子宁愿
        # 用web起个后端服务，用消息队列中转屏幕数据和键盘数据，也坚决不用
        # pyqt
        # 用web做这个多简单啊，随随便便就能搞定。
        # 也不知道这么倒霉，入了tkinter的坑。2天刚学会就要放弃。
        # 得出的结论是：tkinter只适合做非常简单的项目，比如说什么，算了
        # 这就是个连玩具都算不上的东西
        # 一开始我还夸呢，真简单，tkinter后面越来越坑了
        pw = tkinter.PanedWindow(master)
        return pw

    def show(self):
        self._body.mainloop()


if __name__ == '__main__':
    a = App()
    a.show()
