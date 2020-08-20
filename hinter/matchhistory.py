from tkinter import *

import hinter
import hinter.ui.main


class MatchHistory:
    games = []
    rank = ""
    average_kda = ""
    level = 0
    icon = 0
    username = ""

    def __init__(self):
        # Load summoner information
        user = hinter.struct.user.User(hinter.settings.active_user)

        # Don't fail on match list loading just because there is not active user selected
        if not user.user_exists:
            return

        # Load match history information
        entries = hinter.watcher.match.matchlist_by_account(
            hinter.settings.settings.region,
            user.account_id
        )
        for match in entries['matches'][0:5]:
            match = hinter.watcher.match.by_id(hinter.settings.region, match['gameId'])
            text = Label(hinter.ui.main.UI.root, text=match['gameId'])
            text.pack()
