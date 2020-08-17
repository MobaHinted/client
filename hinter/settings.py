import os.path
import hinter.ui.main


class Settings:
    settings_file = './data/settings.dat'
    region = 'na1'
    active_user = ''

    def load_settings(self):
        # Verify folder and file exist
        if not os.path.exists('./data/'):
            os.mkdir('./data')

        if not os.path.exists(self.settings_file):
            open(self.settings_file, "w+")
            return

        settings_file = open(self.settings_file, "r").readlines()

        for setting in settings_file:
            # Skip blank lines
            if setting == '\n':
                continue

            setting = setting.split('=')
            attribute = setting[0]
            value = setting[1].split('\n')[0]

            if getattr(self, attribute, False) != False:
                setattr(self, attribute, value)

    def write_setting(self, setting, value):
        # Remove the setting if currently set
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

        # Reload settings file and menu bar
        self.load_settings()
        hinter.ui.main.UI.add_menu()


settings = Settings()
