import os
from typing import List, Union

import hinter


class Users:
    users_list = hinter.data.constants.PATH_USERS_FILE
    current_list_cache: List[hinter.User.User] = []  # TODO: only list users on the region

    def list_users(self, ui=None) -> List[hinter.User.User]:
        if not os.path.exists(self.users_list):
            open(self.users_list, 'w+')
            return []

        # Read user file
        user_list_file = open(self.users_list, 'r').readlines()
        user_list = []

        # Load users from file
        for username in user_list_file:
            username = username.split('\n')[0]
            user = hinter.User.User(username)

            if user.user_exists:
                user_list.append(
                    hinter.User.User(username)
                )
            elif ui is not None:
                self.remove_user(ui, username)

        # Save user list
        self.current_list_cache = user_list

        return user_list

    def add_user(self, ui, username: str = '') -> Union[bool, None]:
        # Make sure the username popup can close itself
        def close_popup():
            ui.imgui.delete_item(item='add-user')
            ui.imgui.delete_item(item='add-user-input')
            ui.imgui.delete_item(item='add-user-spacer')
            ui.imgui.delete_item(item='add-user-button')

        # Retry the function, with the provided username
        def submit(sender, data):
            # Correct the data-source if the button was used
            if sender == 'add-user-button':
                data = ui.imgui.get_value('add-user-input')

            # Re-run the method, with a username
            close_popup()
            self.add_user(ui, data)

        if username == '':
            # Grab username in a popup
            width = 165
            height = 100
            with ui.imgui.window(
                    label='Add a User',
                    modal=True,
                    tag='add-user',
                    width=width,
                    height=height,
                    no_resize=True,
                    no_move=True,
                    no_collapse=True,
                    on_close=close_popup
            ):
                ui.imgui.add_input_text(
                    tag='add-user-input',
                    parent='add-user',
                    on_enter=True,
                    callback=submit,
                    width=width,
                    hint='League Name',
                )
                ui.imgui.add_spacer(tag='add-user-spacer', height=10)
                ui.imgui.add_button(
                    tag='add-user-button',
                    parent='add-user',
                    label='Add',
                    callback=submit,
                    width=width,
                )
            ui.center_window('add-user', [width, height])
            return

        # Check for duplicate in current user list
        for user in self.current_list_cache:
            if user.username == username:
                ui.show_info_popup(
                    'Duplicate username',
                    'This account is already in your list!'
                )
                return False

        # Check user exists on Riot's side
        user = hinter.User.User(username)
        if not user.user_exists:
            ui.show_info_popup(
                'Nonexistent user',
                'This account does not exist in this region!'
            )
            return False

        # Add to user list file and current list
        user_file = open(self.users_list, 'a+')
        user_file.write(
            user.username + '\n'
        )
        user_file.close()
        self.current_list_cache.append(user)

        # Redraw the menu
        ui.add_menu()
        return True

    def remove_user(self, ui, username: str = ''):
        # Make sure the username popup can close itself
        def close_popup():
            ui.imgui.delete_item(item='remove-user')
            ui.imgui.delete_item(item='remove-user-input')
            ui.imgui.delete_item(item='remove-user-spacer')
            ui.imgui.delete_item(item='remove-user-button')

        # Retry the function, with the provided username
        def submit(sender, data):
            # Correct the data-source if the button was used
            if sender == 'remove-user-button':
                data = ui.imgui.get_value('remove-user-input')

            # Re-run the method, with a username
            close_popup()
            self.remove_user(ui, data)

        # Grab username
        if username == '':
            width = 165
            height = 100
            with ui.imgui.window(
                    label='Remove a User',
                    modal=True,
                    tag='remove-user',
                    width=width,
                    height=height,
                    no_resize=True,
                    no_move=True,
                    no_collapse=True,
                    on_close=close_popup
            ):
                ui.imgui.add_input_text(
                    tag='remove-user-input',
                    parent='remove-user',
                    on_enter=True,
                    callback=submit,
                    width=width,
                    hint='League Name',
                )
                ui.imgui.add_spacer(tag='remove-user-spacer', height=10)
                ui.imgui.add_button(
                    tag='remove-user-button',
                    parent='remove-user',
                    label='Remove',
                    callback=submit,
                    width=width,
                )
            ui.center_window('remove-user', [width, height])
            return

        removed = False

        # Check if user is in list
        found = False
        for user in self.current_list_cache:
            if user.username == username:
                found = True
        if not found:
            ui.show_info_popup(
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
            ui.show_info_popup(
                'Nonexistent username',
                'This account could not be found, and has not been removed!'
            )
            return

        # Reopen file with write permissions
        user_list_file = open(self.users_list, "w+")

        # Write all the recorded lines
        for line in lines:
            user_list_file.write(line)

        user_list_file.close()

        # Confirm user was removed and reload menu
        ui.show_info_popup(
            'User removed',
            'This account was removed!'
        )

        # Redraw the menu
        ui.add_menu()

    # noinspection PyMethodMayBeStatic
    def select_user(self, username: str):
        # Write the variable to have an active user
        hinter.settings.write_setting(
            'active_user',
            username
        )
