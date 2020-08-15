import os.path
from dotenv import load_dotenv
from riotwatcher import LolWatcher
from tkinter import *

import hinter.settings
import hinter.ui.main

load_dotenv('.env')

watcher = LolWatcher(os.getenv('riotKey'))

# hinter.settings.settings.active_user


class Home:
    games = []
    rank = ""
    average_kda = ""
    level = 0
    icon = 0
    username = ""

    def __init__(self):
        # Load summoner information
        summoner = watcher.summoner.by_account(
            hinter.settings.settings.region,
            hinter.settings.settings.active_user_id
        )
        self.level = summoner['summonerLevel']
        self.icon = summoner['profileIconId']
        self.username = summoner['name']

        # Load match history information
        entries = watcher.match.matchlist_by_account(
            hinter.settings.settings.region,
            hinter.settings.settings.active_user_id
        )
        for match in entries['matches'][0:5]:
            match = watcher.match.by_id(hinter.settings.settings.region, match['gameId'])
            print(match)
            text = Label(hinter.ui.main.UI.root, text=match['gameId'])
            text.pack()


home = Home()
