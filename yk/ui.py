import tkinter
import tkinter.messagebox


class App(object):
    def __init__(self):
        self.body()

    def body(self):
        self._body = tkinter.Tk()
        self._body.configure(background='gray')

        self.pingmu_div(self._body)
        self.term_div(self._body)
        self.target_div(self._body)

    def pingmu_div(self, master):
        pass

    def term_div(self, master):
        pass

    def target_div(self, master):
        pass
