#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #
import datetime
import os

from dotenv import load_dotenv

import hinter


# noinspection PySimplifyBooleanCheck
class Settings:
    settings_file = hinter.data.constants.PATH_SETTINGS_FILE
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

    _pipeline_private = 'Private'
    _pipeline_fast = 'Fast'

    pipeline: str = _pipeline_fast

    pipeline_defaulted: bool = False
    # TODO: Add actual cassiopeia settings
    pipelines = {
        'Private': {
            'description': 'Riot Data > Riot (must use your own key)',
        },
        'Fast': {
            'description': 'Riot Data > MobaHinted Proxy > Riot',
        },
    }
    telemetry: bool = False

    def load_settings(self, refresh: bool = False):
        # Skip loading of settings if they are already loaded
        if not refresh and self.settings_loaded:
            print('hinter.Settings: settings already loaded')
            return

        # If there are no settings written, return default settings
        if hinter.data.management.file_empty(hinter.data.constants.PATH_SETTINGS_FILE):
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
                if setting_name != setting:
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

    @property
    def cassiopeia_settings_for_pipeline(self):
        # Setting up the path for cassiopeia
        windows_path = hinter.data.constants.PATH_CASSIOPEIA.split('/')
        cassiopeia_path = os.getcwd() + '\\' + '\\'.join(windows_path[1:3])

        # region Initial pipeline settings that will be added to
        default_pipeline_settings = {
            'Cache': {},
            'SimpleKVDiskStore': {
                'package': 'cassiopeia_diskstore',
                'path': cassiopeia_path,
                'expirations': {
                    'RealmDto': datetime.timedelta(days=3),
                    'VersionListDto': datetime.timedelta(hours=1),
                    'ChampionDto': datetime.timedelta(days=10),
                    'ChampionListDto': datetime.timedelta(hours=1),
                    'RuneDto': datetime.timedelta(days=10),
                    'RuneListDto': datetime.timedelta(hours=1),
                    'ItemDto': datetime.timedelta(days=3),
                    'ItemListDto': datetime.timedelta(hours=1),
                    'SummonerSpellDto': datetime.timedelta(days=10),
                    'SummonerSpellListDto': datetime.timedelta(days=3),
                    'MapDto': datetime.timedelta(days=3),
                    'MapListDto': datetime.timedelta(days=3),
                    'ProfileIconDetailsDto': datetime.timedelta(days=10),
                    'ProfileIconDataDto': datetime.timedelta(days=3),
                    'LanguagesDto': datetime.timedelta(days=10),
                    'LanguageStringsDto': datetime.timedelta(days=10),
                    'ChampionRotationDto': datetime.timedelta(days=1),
                    'ChampionMasteryDto': datetime.timedelta(hours=3),
                    'ChampionMasteryListDto': datetime.timedelta(days=3),
                    'ChallengerLeagueListDto': datetime.timedelta(hours=6),
                    'GrandmasterLeagueListDto': datetime.timedelta(hours=6),
                    'MasterLeagueListDto': datetime.timedelta(hours=6),
                    'MatchDto': -1,
                    'TimelineDto': -1,
                    'SummonerDto': datetime.timedelta(days=1),
                    'ShardStatusDto': datetime.timedelta(hours=1),
                    'CurrentGameInfoDto': datetime.timedelta(minutes=10),
                    'FeaturedGamesDto': datetime.timedelta(hours=2),
                    'PatchListDto': datetime.timedelta(hours=3)
                }
            },
        }
        # endregion Initial pipeline settings that will be added to

        # Verify that the Private pipeline will work if selected
        no_env_file = not os.path.exists('.env') or hinter.data.management.file_empty('.env')
        if no_env_file and self.pipeline == self._pipeline_private:
            self.pipeline_defaulted = True
            self.write_setting('pipeline', self._pipeline_fast)
            self.pipeline = self._pipeline_fast

        # Give settings specific to each pipeline
        match self.pipeline:
            case self._pipeline_private:
                # TODO: Add Champion.gg
                print('USING: Development Key (RIOT\'s servers)')

                load_dotenv('.env')

                pipeline_settings = default_pipeline_settings | {
                    'DDragon': {},
                    'RiotAPI': {
                        'api_key': os.getenv('RIOT_API_KEY'),
                    },
                }
            case self._pipeline_fast:
                print('USING: Kernel (zbee\'s servers)')

                pipeline_settings = default_pipeline_settings | {
                    'Kernel': {
                        'server_url': 'https://mhk-api.zbee.dev',
                        'port': '443',
                    },
                    'DDragon': {}
                }

        # Fill in the few other cassiopeia settings
        settings = {
            "global": {
                "version_from_match": "version",
                "default_region": hinter.settings.region
            },
            'pipeline': pipeline_settings,
        }

        return settings
