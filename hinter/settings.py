#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import os.path
import time
from hinter.data.constants import PATH_SETTINGS_FILE, PATH_DATA


# noinspection PySimplifyBooleanCheck
class Settings:
    settings_file = PATH_SETTINGS_FILE
    settings_loaded = False
    version = '0.0.0'
    x: int = 10  # Window Position
    y: int = 10
    default_width: int = 1780  # Default Window Size
    default_height: int = 670
    width: int = 1780  # Window Size
    height: int = 670

    # Settings Popup settings
    overlay_milestones: bool = False
    overlay_cs_tracker: bool = True
    overlay_objectives: bool = False
    overlay_spell_tracker: bool = True
    overlay_jungle: bool = True
    overlay_aram: bool = True
    overlay_duos: bool = True
    overlay_gold_diff: bool = True
    overlay_map_check: bool = False
    overlay_back_reminder: bool = False
    overlay_trinket: bool = True
    overlay_counter_items: bool = False

    launch_on_startup: bool = False
    automatic_updates: bool = True
    close_to_tray: bool = False
    bring_to_front: bool = False
    save_window_position: bool = True
    detect_new_accounts: bool = True

    match_history_count: int = 50
    friend_threshold: int = 5

    show_my_rank: bool = True
    show_ally_rank: bool = True
    show_enemy_rank: bool = True
    show_game_ranks: bool = True

    show_current_session: bool = False
    show_pregame_separate: bool = False
    auto_close_pregame: bool = False
    show_builds_separate: bool = False
    auto_close_builds: bool = True
    show_postgame_separate: bool = False

    active_user: str = ''  # TODO: What if this was scrapped and only detected the active user?
    region: str = 'NA'

    pipeline: str = 'Fast, Accurate'
    # TODO: Add actual cassiopeia settings
    pipelines = {
        'Most Private': {
            'description': 'Riot Data > Riot (recommended to use your own key)',
            'cassiopeia_setting': {}
        },
        'Private, Fast': {
            'description': 'Riot Data > MobaHinted Proxy > Riot',
            'cassiopeia_setting': {}
        },
        'Fast, Accurate': {
            'description': 'Community Data > MobaHinted Proxy > Riot',
            'cassiopeia_setting': {}
        },
    }
    telemetry: bool = False

    def load_settings(self, refresh: bool = False):
        # Skip loading of settings if they are already loaded
        if not refresh and self.settings_loaded:
            print('hinter.Settings: settings already loaded')
            return

        # Verify folder and file exist
        if not os.path.exists(PATH_DATA):
            os.mkdir(PATH_DATA)
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

    # noinspection PyMethodMayBeStatic
    def is_file_older_than_x_days(self, file, days=1):
        file_time = os.path.getmtime(file)
        # Check against 24 hours
        return (time.time() - file_time) / 3600 > 24*days
