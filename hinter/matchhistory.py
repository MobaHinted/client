import os.path
from dotenv import load_dotenv
from riotwatcher import LolWatcher
from tkinter import *

import hinter.settings
import hinter.ui.main
import hinter.background.dataloader
import hinter.struct.user

load_dotenv('.env')

watcher = LolWatcher(os.getenv('riotKey'))


class MatchHistory:
    games = []
    rank = ""
    average_kda = ""
    level = 0
    icon = 0
    username = ""

    def __init__(self):
        # Load summoner information
        user = hinter.struct.user.User(hinter.settings.settings.active_user)

        # Don't fail on matchlist loading just because there is not active user selected
        if not user.user_exists:
            return

        # Load match history information
        entries = watcher.match.matchlist_by_account(
            hinter.settings.settings.region,
            user.account_id
        )
        for match in entries['matches'][0:5]:
            match = watcher.match.by_id(hinter.settings.settings.region, match['gameId'])
            text = Label(hinter.ui.main.UI.root, text=match['gameId'])
            text.pack()


match_history = MatchHistory()
