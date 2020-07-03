import tkinter

import hinter.users
import hinter.settings


class UI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.state('zoomed')
        self.root.title('MobaHinted')
        self.root.iconbitmap("./assets/logo.ico")
        self.add_menu()

    def add_menu(self):
        # Create base menu
        menu = tkinter.Menu(self.root)

        # Create file dropdown
        file_menu = tkinter.Menu(self.root)
        file_menu.add_command(
            label="Exit",
            command=lambda: self.quit()
        )
        menu.add_cascade(label="File", menu=file_menu)

        # Create user dropdown
        user_menu = tkinter.Menu(self.root)
        menu.add_cascade(label="User", menu=user_menu)
        user_menu.add_command(
            label="Add user",
            command=lambda: hinter.users.users.add_user(self.root)
        )

        # Add users to dropdown
        user_list = hinter.users.users.list_users()

        if len(user_list) > 0:
            user_menu.add_command(
                label="Remove user",
                command=lambda:
                hinter.users.users.remove_user(self.root)
            )
            user_menu.add_separator()

        for user in user_list:
            username = user[0]
            if user[0] == hinter.settings.settings.active_user:
                username = '* ' + username

            user_menu.add_command(
                label=username,
                command=lambda: hinter.users.users.select_user(user)
            )

        # Add the menus
        self.root.config(menu=menu)

    def quit(self):
        self.root.destroy()


UI = UI()
