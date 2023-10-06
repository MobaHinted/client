import os.path


# noinspection PySimplifyBooleanCheck
class Settings:
    settings_file = './data/settings.dat'
    region = 'NA'
    active_user = ''
    settings_loaded = False
    version = '0.0.0'
    x: int = 10  # Window Position
    y: int = 10
    default_width: int = 1780  # Default Window Size
    default_height: int = 670
    width: int = 1780  # Window Size
    height: int = 670

    def load_settings(self, refresh: bool = False):
        # Skip loading of settings if they are already loaded
        if not refresh and self.settings_loaded:
            print('hinter.Settings: settings already loaded')
            return

        # Verify folder and file exist
        if not os.path.exists('./data/'):
            os.mkdir('./data')
        if not os.path.exists(self.settings_file):
            open(self.settings_file, 'w+')
            return

        # Open settings file
        settings_file = open(self.settings_file, 'r').readlines()

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
            if getattr(self, attribute, None) is not None:
                if value == 'False':
                    value = False
                elif value == 'True':
                    value = True
                elif value.lstrip('-').isnumeric():
                    value = int(value)

                setattr(self, attribute, value)

        # Save a setting that the settings were loaded
        self.settings_loaded = True

    def write_setting(self, setting, value):
        # Verify folder and file exist
        if not os.path.exists('./data/'):
            os.mkdir('./data')
        if not os.path.exists(self.settings_file):
            open(self.settings_file, 'w+')
            return

        # Remove the setting if currently set
        if getattr(self, setting, None) is not None:
            settings_file_original = open(self.settings_file, 'r').readlines()
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
            settings_file = open(self.settings_file, 'w+')

            # Write all the recorded lines
            for line in lines:
                settings_file.write(line)

            settings_file.close()

        # Add the setting
        settings_file = open(self.settings_file, 'a+')
        settings_file.write(f'{setting}={value}\n')
        settings_file.close()

        # Reload settings file
        self.load_settings(refresh=True)
