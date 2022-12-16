import tkinter
import tkinter.messagebox


class PingmuDiv(tkinter.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        tkinter.Frame.__init__(self, master, cnf, **kw)
        self._frame_count = 0

    def painting(self, width, height):
        self._width = width
        self._canvas = tkinter.Canvas(self, width=width, height=height)
        self._canvas.grid(row=0, column=0)
        self._sb = tkinter.Scrollbar(self, orient='vertical', command=self.yview)
        self._sb.grid(row=0, column=1)
        self._canvas.configure(yscrollcommand=self._sb.set)

    def add_pingmu(self, width, height):
        f = tkinter.Frame(self._canvas, bd=1, relief='solid')
        self._canvas.create_window(0, (self._frame_count * 200), window=f,
                                   width=width, height=height)
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
