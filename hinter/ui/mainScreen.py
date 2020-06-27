import tkinter


class UI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.state('zoomed')
        self.root.title('MobaHinter')
        self.root.iconbitmap("./assets/logo.ico")

    def quit(self):
        self.root.destroy()


app = UI()
