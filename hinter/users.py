from tkinter import simpledialog


class Users:
    def add_user(self, root, menu):
        username = simpledialog.askstring(
            "Add User",
            "NA region only. What is your username?",
            parent=root
        )
        menu.add_command(
            label=username,
            command=lambda: self.select_user(username)
        )

    def select_user(self, username):
        print(username)


users = Users()
