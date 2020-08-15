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

        # Add option to remove users if there are any
        if len(user_list) > 0:
            user_menu.add_command(
                label="Remove user",
                command=lambda:
                hinter.users.users.remove_user(self.root)
            )
            user_menu.add_separator()

        # List users, with on-click to select that as the active user
        for user in user_list:
            # Set the username for the label of the dropdown entry
            username = user[0]
            # Check if the user is the currently active selection
            if user[0] == hinter.settings.settings.active_user:
                username = '* ' + username

            # Add the user entry
            user_menu.add_command(
                label=username,
                command=lambda user_info=user:  # lambda parameter required for user data to be static
                hinter.users.users.select_user(user_info)  # method to set this user as active if entry is clicked
            )

        # Add the menus
        self.root.config(menu=menu)

    def quit(self):
        self.root.destroy()


UI = UI()
