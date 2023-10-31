#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import os
import pickle

import cassiopeia
# noinspection PyUnresolvedReferences
import cassiopeia_diskstore  # Required for building to executable
from dotenv import load_dotenv

# noinspection PyUnresolvedReferences
import dearpygui.dearpygui as imgui  # For all the modules to use

import roleidentification as casiopeia_role_identification

# noinspection PyUnresolvedReferences
import hinter.data

# noinspection PyUnresolvedReferences
import hinter.settings
# noinspection PyUnresolvedReferences
import hinter.struct.User as User
# noinspection PyUnresolvedReferences
import hinter.struct.PlayerPlayedWith as PlayerPlayedWith
# noinspection PyUnresolvedReferences
import hinter.struct.PlayersPlayedWith as PlayersPlayedWith
# noinspection PyUnresolvedReferences
import hinter.background.dataloader as DataLoader
# noinspection PyUnresolvedReferences
import hinter.ui
# noinspection PyUnresolvedReferences
import hinter.ui.progress as Progress
from hinter.ui.functionality import UIFunctionality
# noinspection PyUnresolvedReferences
import hinter.ui.popups as Popups
import hinter.users
from hinter.ui.menu import UIMenus
# noinspection PyUnresolvedReferences
from hinter.background.match_data import MatchData as MatchData
# noinspection PyUnresolvedReferences
from hinter.background.match_data import GameReturn as GameData
# noinspection PyUnresolvedReferences
from hinter.match_breakdown import MatchBreakdown as MatchBreakdown

# TODO: Move MatchHistory here

UI: UIFunctionality
Menu: UIMenus = hinter.UIMenus()

# Set up settings
settings = hinter.settings.Settings()
settings.load_settings()

# region Champion Role Data
# Check if we need to update the champion role data
want_new_champion_role_data = hinter.data.management.Clean.is_file_older_than_x_days(
    hinter.data.constants.PATH_CHAMPION_ROLE_DATA_FILE,
    2
)

# If we do need to get fresh data
if want_new_champion_role_data:
    # Get the data
    ChampionRoleData = casiopeia_role_identification.pull_data()
    # Cache the data for 2 days
    with open(hinter.data.constants.PATH_CHAMPION_ROLE_DATA_FILE, 'wb') as role_data_file:
        pickle.dump(ChampionRoleData, role_data_file, pickle.HIGHEST_PROTOCOL)
else:
    # Load the cached champion role data if we have it and it's fresh
    with open(hinter.data.constants.PATH_CHAMPION_ROLE_DATA_FILE, 'rb') as role_data_file:
        ChampionRoleData = pickle.load(role_data_file)

del want_new_champion_role_data
# endregion Champion Role Data

# region Casiopeia-Diskstore path
# Get ready for Cassiopeia
windows_path = hinter.data.constants.PATH_CASSIOPEIA.split('/')
cassiopeia_path = os.getcwd() + '\\' + '\\'.join(windows_path[1:3])
# endregion Casiopeia-Diskstore path

# TODO: load pipeline from settings
cassiopeia_settings = {
    "global": {
        "version_from_match": "version",
        "default_region": hinter.settings.region
    },
    'pipeline': {
        'Cache': {},
        "SimpleKVDiskStore": {
            "package": "cassiopeia_diskstore",
            "path": cassiopeia_path
        },
        'DDragon': {},
    },
}

# region Cassiopeia pipeline settings
# Set up Cassiopeia, either with local key or proxy kernel
try:
    if not os.path.exists('.env'):
        raise Exception('No .env file found')

    load_dotenv('.env')
    cassiopeia.set_riot_api_key(os.getenv('RIOT_API_KEY'))
    cassiopeia_settings['pipeline']['RiotAPI'] = {
        'api_key': os.getenv('RIOT_API_KEY'),
    }
    print('USING: Development Key (RIOT\'s servers)')
except Exception:
    cassiopeia_settings['pipeline']['Kernel'] = {
            'server_url': 'https://mhk-api.zbee.dev',
            'port': '443',
        }
    print('USING: Kernel with key (zbee\'s servers)')

# Load basic settings for Cassiopeia
cassiopeia.apply_settings(cassiopeia_settings)
# endregion Cassiopeia pipeline settings

# Set up user control
users = hinter.users.Users()
