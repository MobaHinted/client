import os
from dotenv import load_dotenv

from riotwatcher import LolWatcher

import hinter.settings
import hinter.users

import hinter.struct.user

# Set up riotWatcher
load_dotenv('.env')
watcher = LolWatcher(os.getenv('riotKey'))

# Set up settings
settings = hinter.settings.Settings()
settings.load_settings()

# Set up user control
users = hinter.users.Users()
