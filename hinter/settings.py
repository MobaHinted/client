import os.path

import cassiopeia
import dearpygui.dearpygui


# noinspection PySimplifyBooleanCheck
class Settings:
    settings_file = './data/settings.dat'
    region = 'NA'
    active_user = ''
    settings_loaded = False
    imgui: dearpygui.dearpygui = dearpygui.dearpygui
    version = '0.0.0'

    def ready_settings_window(self):
        # Make sure the popup can be hidden
        def close_popup():
            self.imgui.hide_item(item='settings-popup')

        # Show the popup
        with self.imgui.window(
                label='Settings',
                modal=True,
                tag='settings-popup',
                width=600,
                height=500,
                no_resize=True,
                no_move=True,
                no_collapse=True,
                on_close=close_popup,
                show=False,
        ):
            # users = hinter.users.list_users()

            with self.imgui.table(header_row=False, no_clip=True):
                self.imgui.add_table_column()
                self.imgui.add_table_column()
                self.imgui.add_table_column()
                self.imgui.add_table_column()
                with self.imgui.table_row():
                    self.imgui.add_text("Current User:")
                    self.imgui.add_text(self.active_user)
                    # self.imgui.add_combo(items=[e.username for e in users], default_value=self.active_user)
                    self.imgui.add_text("Current Region:")
                    self.imgui.add_text(self.region)
                    # self.imgui.add_combo(items=[e.value for e in cassiopeia.data.Region], default_value=self.region)
                with self.imgui.table_row():
                    self.imgui.add_spacer()
                with self.imgui.table_row():
                    self.imgui.add_text("About")
                with self.imgui.table_row():
                    self.imgui.add_text("League Patch:")
                    self.imgui.add_text(cassiopeia.get_version(region=self.region))
                    self.imgui.add_text("Mobahinted Ver.:")
                    self.imgui.add_text(self.version)

    def load_settings(self, refresh: bool = False):
        # Skip loading of settings if they are already loaded
        if not refresh and self.settings_loaded:
            print('hinter.Settings: settings already loaded')
            return

        # Verify folder and file exist
        if not os.path.exists('./data/'):
            os.mkdir('./data')
        if not os.path.exists(self.settings_file):
            open(self.settings_file, "w+")
            return

        # Open settings file
        settings_file = open(self.settings_file, "r").readlines()

        # Read settings file
        for setting in settings_file:
            # Skip blank lines
            if setting == '\n':
                continue

            # Read the setting into variables
            setting = setting.split('=')
            attribute = setting[0]
            value = setting[1].split('\n')[0]

            # Save the setting to the Class
            # This has to be verbose otherwise falsey values will trip it
            if getattr(self, attribute, False) != False:
                setattr(self, attribute, value)

        # Save a setting that the settings were loaded
        self.settings_loaded = True

    def write_setting(self, setting, value):
        # Remove the setting if currently set
        # This has to be verbose otherwise falsey values will trip it
        if getattr(self, setting, False) != False:
            settings_file_original = open(self.settings_file, "r").readlines()
            lines = []

            # Go through list
            for line in settings_file_original:
                # Skip blank lines
                if line == '\n':
                    continue

                # Check setting in list
                setting_name = line.split('=')[0]
                # If the setting name matches the one wanting updated
                # then don't record it
                if setting_name == setting:
                    removed = True
                else:
                    lines.append(line)

            # Reopen file with write permissions
            settings_file = open(self.settings_file, "w+")

            # Write all the recorded lines
            for line in lines:
                settings_file.write(line)

            settings_file.close()

        # Add the setting
        settings_file = open(self.settings_file, 'a+')
        settings_file.write(
            setting + '=' + value + '\n'
        )
        settings_file.close()

        # Reload settings file
        self.load_settings(refresh=True)
