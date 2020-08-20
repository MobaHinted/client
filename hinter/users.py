import os
from typing import List
from tkinter import messagebox
from tkinter import simpledialog

import hinter.ui.main
import hinter.struct.user


class Users:
    users_list = './data/users.dat'
    current_list_cache: List[hinter.struct.user.User] = []

    def list_users(self, root):
        # Open user file
        if not os.path.exists('./data/'):
            os.mkdir('./data')

        if not os.path.exists(self.users_list):
            open(self.users_list, 'w+')
            return []

        # Read user file
        user_list_file = open(self.users_list, 'r').readlines()
        user_list = []

        # Load users from file
        for username in user_list_file:
            username = username.split('\n')[0]
            user = hinter.struct.user.User(username)

            if user.user_exists:
                user_list.append(
                    hinter.struct.user.User(username)
                )
            else:
                self.remove_user(root, username)

        # Save user list
        self.current_list_cache = user_list

        return user_list

    def add_user(self, root):
        # Grab username
        username = simpledialog.askstring(
            'Add User',
            'What is the username? (currently using region: '
            + hinter.settings.region + ')',
            parent=root
        )

        # Check for duplicate in current user list
        for user in self.current_list_cache:
            if user.username == username:
                messagebox.showwarning(
                    'Duplicate username',
                    'This account is already in your list!'
                )
                return

        # Check user exists on Riot's side
        user = hinter.struct.user.User(username)
        if not user.user_exists:
            messagebox.showwarning(
                'Nonexistent user',
                'This account does not exist in this region!'
            )
            return

        # Add to user list file and current list
        user_file = open(self.users_list, 'a+')
        user_file.write(
            user.username + '\n'
        )
        user_file.close()
        self.current_list_cache.append(user)

        # Add to dropdown menu
        hinter.ui.main.UI.add_menu()

    def remove_user(self, root, username: str = ''):
        # Grab username
        if username == '':
            username = simpledialog.askstring(
                'Remove User',
                'What username do you want removed?',
                parent=root
            )

        removed = False

        # Check if user is in list
        found = False
        for user in self.current_list_cache:
            if user.username == username:
                found = True
        if not found:
            messagebox.showwarning(
                'Nonexistent username',
                'This account was never added, and has not been removed!'
            )
            return

        # Open users list
        user_list_file_original = open(self.users_list, "r").readlines()
        lines = []

        # Go through list
        for line in user_list_file_original:
            # Check username in list
            listed_name = line.split('\n')[0]
            # If the username matches the one wanting removed then don't record it
            if listed_name == username:
                removed = True
            else:
                lines.append(line)

        # Throw an error if nothing could be removed
        if not removed:
            messagebox.showwarning(
                'Nonexistent username',
                'This account could not be found, and has not been removed!'
            )
            hinter.ui.main.UI.add_menu()
            return

        # Reopen file with write permissions
        user_list_file = open(self.users_list, "w+")

        # Write all the recorded lines
        for line in lines:
            user_list_file.write(line)

        user_list_file.close()

        # Confirm user was removed and reload menu
        messagebox.showinfo(
            'User removed',
            'This account was removed!'
        )
        hinter.ui.main.UI.add_menu()

    def select_user(self, username: str):
        # Write the variable to have an active user
        hinter.settings.write_setting(
            'active_user',
            username
        )
