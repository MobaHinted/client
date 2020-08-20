import os.path
from dotenv import load_dotenv
from riotwatcher import LolWatcher

import hinter.settings
import hinter.ui.main
import hinter.background.dataloader

load_dotenv('.env')

watcher = LolWatcher(os.getenv('riotKey'))


class User:
    user_exists: bool = None
    username: str = ''
    account_id: str = ''
    level: int = 0
    icon: str = ''

    def __init__(self, username: str):
        # Check user exists on Riot's side
        try:
            user = watcher.summoner.by_name(
                hinter.settings.settings.region,
                username
            )
        except Exception as e:
            self.user_exists = False
            return

        # Load in data
        self.user_exists = True
        self.username = user['name']
        self.account_id = user['accountId']
        self.level = user['summonerLevel']
        self.icon = user['profileIconId']
