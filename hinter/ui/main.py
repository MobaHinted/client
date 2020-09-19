import tkinter

import hinter
import hinter.background.dataloader


class UI:
    screen: tkinter.Frame

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
            label="Reload all data",
            command=lambda: hinter.background.dataloader.data_loader.load_all(
                refresh=True
            )
        )
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
            command=lambda: (hinter.users.add_user(self.root), self.add_menu())
        )

        # Add users to dropdown
        user_list = hinter.users.list_users(self.root)

        # Add separation
        if len(user_list) > 0:
            user_menu.add_separator()

        # List users, with on-click to select that as the active user
        for user in user_list:
            # Set the username for the label of the dropdown entry
            username = user.username
            # Check if the user is the currently active selection
            if username == hinter.settings.active_user:
                username = '* ' + username

            # Add the user entry
            user_menu.add_command(
                label=username,
                command=lambda user_info=user.username:       # lambda parameter required for user data to be static
                (
                    hinter.users.select_user(user.username),  # method to set this user as active if entry is clicked
                    self.add_menu()                           # Refresh menu
                )
            )

        # Add option to remove users
        if len(user_list) > 0:
            user_menu.add_separator()
            user_menu.add_command(
                label="Remove user",
                command=lambda:
                hinter.users.remove_user(self.root)
            )

        # Add the menus
        self.root.config(menu=menu)

    def new_screen(self):
        self.screen = tkinter.Frame(self.root)

    def clear_screen(self):
        self.screen.destroy()

    def quit(self):
        self.root.destroy()


UI = UI()
