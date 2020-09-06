from tkinter import *

import hinter
import hinter.ui.main
import hinter.struct.user

import cassiopeia


class MatchHistory:
    games: cassiopeia.MatchHistory = []
    rank: cassiopeia.Rank = ""
    average_kda = ""
    level = 0
    icon = 0
    username = ""

    def __init__(self, user: hinter.struct.user.User = None):
        # Load summoner information
        if user is not None:
            user = cassiopeia.get_summoner(name=user.username)
        else:
            user = cassiopeia.get_summoner(name=hinter.settings.active_user)

        # Save variables
        self.games = user.match_history
        self.rank = user.ranks[cassiopeia.Queue.ranked_solo_fives]
        self.level = user.level
        self.icon = user.profile_icon

        # Load match history information
        entries: cassiopeia.MatchHistory = user.match_history

        for match in entries[0:5]:
            match: cassiopeia.Match
            print(match.id)
            text = Label(hinter.ui.main.UI.root, text=match.id)
            text.pack()
