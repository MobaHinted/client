import tkinter

import hinter.users


class UI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.state('zoomed')
        self.root.title('MobaHinted')
        self.root.iconbitmap("./assets/logo.ico")
        self.add_menu()

    def add_menu(self):
        menu = tkinter.Menu(self.root)
        user_menu = tkinter.Menu(self.root)
        menu.add_cascade(label="User", menu=user_menu)
        user_menu.add_command(
            label="New",
            command=lambda: hinter.users.users.add_user(self.root, user_menu)
        )
        user_menu.add_separator()
        user_menu.add_command(label="Exit", command=self.root)

        self.root.config(menu=menu)

    def quit(self):
        self.root.destroy()


UI = UI()
