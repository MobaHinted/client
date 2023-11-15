#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import pickle

import cassiopeia
# noinspection PyUnresolvedReferences
import cassiopeia_diskstore  # Required for building to executable

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
from hinter.ui.errors import Errors
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
Errors: Errors = hinter.Errors()

# Make sure all files and folders exist
hinter.data.management.Setup()

# Set up settings
settings = hinter.settings.Settings()
settings.load_settings()

# region Champion Role Data
# Check if we need to update the champion role data
want_new_champion_role_data = hinter.data.management.Clean.is_file_older_than_x_days(
    hinter.data.constants.PATH_CHAMPION_ROLE_DATA_FILE,
    2
)
# Check if the file is empty
if hinter.data.management.file_empty(hinter.data.constants.PATH_CHAMPION_ROLE_DATA_FILE):
    want_new_champion_role_data = True

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

cassiopeia.apply_settings(settings.cassiopeia_settings_for_pipeline)

# Set up user control
users = hinter.users.Users()
