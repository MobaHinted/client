import os
import os.path
from tkinter import messagebox
from tkinter import simpledialog

from dotenv import load_dotenv
from riotwatcher import LolWatcher

import hinter.settings
import hinter.ui.main

load_dotenv('.env')

watcher = LolWatcher(os.getenv('riotKey'))


class Users:
    users_list = './data/users.dat'
    current_list_cache = []

    def __init__(self):
        # Make sure settings are loaded
        hinter.settings.settings.load_settings()

    def list_users(self):
        # Open user file
        if not os.path.exists('./data/'):
            os.mkdir('./data')

        if not os.path.exists(self.users_list):
            open(self.users_list, "w+")
            return []

        # Read user file
        user_list_file = open(self.users_list, "r").readlines()
        user_list = []

        # Load users from file
        for user in user_list_file:
            user_list.append(
                [user.split(';;')[0], user.split(';;')[1]]
            )

        # Save user list
        self.current_list_cache = user_list

        return user_list

    def add_user(self, root):
        # Grab username
        username = simpledialog.askstring(
            "Add User",
            "What is your username? (currently using region: "
            + hinter.settings.settings.region + ")",
            parent=root
        )

        # Check for duplicate in current user list
        user_list = []
        for user in self.current_list_cache:
            user_list.append(user[0])

        if username in user_list:
            messagebox.showwarning(
                'Duplicate username',
                'This account is already in your list!'
            )
            return

        # Check user exists on Riot's side
        try:
            summoner = watcher.summoner.by_name(
                hinter.settings.settings.region,
                username
            )
        except Exception:
            messagebox.showwarning(
                'Nonexistent user',
                'This account does not exist in this region!'
            )
            return

        # Add to user list
        user_file = open(self.users_list, 'a+')
        user_file.write(
            summoner['name'] + ';;' + summoner['accountId'] + '\n'
        )
        user_file.close()
        self.current_list_cache.append(username)

        # Add to dropdown menu
        hinter.ui.main.UI.add_menu()

    def remove_user(self, root):
        # Grab username
        username = simpledialog.askstring(
            "Remove User",
            "What username do you want removed?",
            parent=root
        )

        removed = False

        # Check if user is in list
        user_list = []
        for user in self.current_list_cache:
            user_list.append(user[0])

        if username not in user_list:
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
            listed_name = line.split(';;')[0]
            # If the username matches the one wanting removed
            # then don't record it
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

    def select_user(self, user):
        # Write both variables for the active user setting
        hinter.settings.settings.write_setting(
            'active_user',
            user[0]
        )
        hinter.settings.settings.write_setting(
            'active_user_id',
            user[1]
        )


users = Users()
