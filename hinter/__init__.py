import os

import cassiopeia
# noinspection PyUnresolvedReferences
import cassiopeia_diskstore  # Required for building to executable
from dotenv import load_dotenv

import dearpygui.dearpygui as imgui  # For all the modules to use

import hinter.settings
import hinter.struct.User as User
import hinter.struct.PlayerPlayedWith as PlayerPlayedWith
import hinter.struct.PlayersPlayedWith as PlayersPlayedWith
import hinter.data
import hinter.background.dataloader as DataLoader
import hinter.ui
import hinter.ui.progress as Progress
from hinter.ui.functionality import UIFunctionality
import hinter.ui.popups as Popups
import hinter.users
from hinter.ui.menu import UIMenus
from hinter.match_breakdown import MatchBreakdown as MatchBreakdown
# noinspection PyUnresolvedReferences

# TODO: Move MatchHistory here

UI: UIFunctionality
Menu: UIMenus

# Set up settings
settings = hinter.settings.Settings()
settings.load_settings()

# Get ready for Cassiopeia
if not os.path.exists(hinter.data.constants.PATH_CASSIOPEIA):
    os.mkdir(hinter.data.constants.PATH_CASSIOPEIA)
windows_path = hinter.data.constants.PATH_CASSIOPEIA.split('/')
cassiopeia_path = os.getcwd() + '\\' + '\\'.join(windows_path[1:3])

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

'''
cassiopeia-diskstore 1.1.3 does not work with v5 endpoints
it is currently monkey-patched to make match history work
https://github.com/meraki-analytics/cassiopeia/issues/384
https://github.com/meraki-analytics/cassiopeia-datastores/pull/27
'''

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

# Set up user control
users = hinter.users.Users()
