#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

__all__ = [
    'URL_ASSETS_ZIP',
    'URL_RANKED_EMBLEMS',
    'URL_KERNEL_PROXY',
    'URL_KERNEL_PROXY_PORT',
    'UI_FONT_SCALE',
    'SUMMONERS_RIFT_MAP_ID',
    'TEAM_BLUE_COLOR',
    'TEAM_RED_COLOR',
    'MATCH_COLOR_REMAKE',
    'MATCH_COLOR_LOSS',
    'MATCH_COLOR_WIN',
    'ICON_SIZE_RANK',
    'ICON_SIZE_SUMMONER',
    'ICON_SIZE_BAN',
    'ICON_SIZE_CHAMPION',
    'ICON_SIZE_SPELL',
    'ICON_SIZE_RUNE',
    'ICON_SIZE_SECONDARY_RUNE',
    'ICON_SIZE_ITEM',
    'IMAGE_TYPE_PIL',
    'IMAGE_TYPE_FILE',
    'IMAGE_TYPE_REMOTE',
    'PATH_ASSETS',
    'PATH_DATA',
    'PATH_CASSIOPEIA',
    'PATH_IMAGES',
    'PATH_RANKED_EMBLEMS',
    'PATH_CHAMPION_ROLE_DATA_FILE',
    'PATH_IMGUI_FILE',
    'PATH_SETTINGS_FILE',
    'PATH_USERS_FILE',
    'PATH_FRIENDS_FILE',
]

URL_ASSETS_ZIP = 'https://codeload.github.com/zbee/mobahinted/zip/refs/heads/master'
URL_RANKED_EMBLEMS = 'https://static.developer.riotgames.com/docs/lol/ranked-emblems-latest.zip'
URL_KERNEL_PROXY = 'https://mhk.zbee.dev'
URL_KERNEL_PROXY_PORT = 443

UI_FONT_SCALE = 2

SUMMONERS_RIFT_MAP_ID = 11

TEAM_BLUE_COLOR = (0, 77, 140, 255)
TEAM_RED_COLOR = (124, 57, 83, 255)

MATCH_COLOR_REMAKE = [255, 255, 255, 10]
MATCH_COLOR_LOSS = [220, 158, 158, 40]
MATCH_COLOR_WIN = [151, 199, 154, 60]

ICON_SIZE_RANK = (60, 60)
ICON_SIZE_SUMMONER = (35, 35)
ICON_SIZE_FRIEND = (30, 30)
ICON_SIZE_BAN = (20, 20)
ICON_SIZE_CHAMPION = (64, 64)
ICON_SIZE_SPELL = (30, 30)
ICON_SIZE_RUNE = (30, 30)
ICON_SIZE_SECONDARY_RUNE = (22, 22)
ICON_SIZE_ITEM = (30, 30)

IMAGE_TYPE_PIL = 'pil'
IMAGE_TYPE_FILE = 'file'
IMAGE_TYPE_REMOTE = 'remote'

PATH_ASSETS = './assets/'
PATH_DATA = './data/'

PATH_CASSIOPEIA = PATH_DATA + 'cassiopeia/'
PATH_IMAGES = PATH_DATA + 'image_cache/'
PATH_RANKED_EMBLEMS = PATH_DATA + 'ranked_emblems/'

PATH_CHAMPION_ROLE_DATA_FILE = PATH_DATA + 'champion_roles.dat'
PATH_IMGUI_FILE = PATH_DATA + 'imgui.ini'
PATH_SETTINGS_FILE = PATH_DATA + 'settings.dat'
PATH_USERS_FILE = PATH_DATA + 'users.dat'
PATH_FRIENDS_FILE = PATH_DATA + 'friends.dat'
