from tkinter import *

import hinter
import hinter.ui.main
import hinter.struct.user

import cassiopeia


class MatchHistory:
    games: cassiopeia.MatchHistory
    games_shown: int = 25
    rank: cassiopeia.Rank
    average_kda: float
    level = 0
    icon = 0
    username = ""
    left_bar: Frame
    history: Frame
    right_bar: Frame

    def __init__(self, user: hinter.struct.user.User = None):
        # Load summoner information
        if user is not None:
            user = cassiopeia.get_summoner(name=user.username)
        else:
            user = cassiopeia.get_summoner(name=hinter.settings.active_user)
        self.username = user.name

        # Save variables
        self.games = user.match_history
        self.rank = user.ranks[cassiopeia.Queue.ranked_solo_fives]
        self.level = user.level
        self.icon = user.profile_icon

        # Set up screen
        hinter.ui.main.UI.new_screen()

        # Load match history information
        self.games = user.match_history

    def show_match_screen(self):
        hinter.ui.main.UI.screen.grid(row=0, column=0, padx=150, pady=20)

        # Set up the left-bar
        self.left_bar = Frame(master=hinter.ui.main.UI.screen)
        text = Label(master=self.left_bar, text='rank, icon, level, lp, users-played-with stats here')
        text.grid()
        self.left_bar.grid(row=0, column=0, padx=20)

        # Set up the right-bar
        self.right_bar = Frame(master=hinter.ui.main.UI.screen)
        text = Label(master=self.right_bar, text='role distribution, champ wr here')
        text.grid()
        self.right_bar.grid(row=0, column=2, padx=20)

        # Set up the main match history, and call to show all matches
        self.history = Frame(master=hinter.ui.main.UI.screen)

        text = Label(master=self.history, text='match history here')
        text.grid()

        self.display_matches()

        # Display match history
        self.history.grid(row=0, column=1, padx=20)

    def display_matches(self):
        # Loop through the first games
        for key, match in enumerate(self.games[0:self.games_shown]):
            # Set up each game's container, and cast multiple variables
            game = Frame(self.history)
            match: cassiopeia.Match
            team: str
            player: cassiopeia.core.match.Participant
            player_stats: cassiopeia.core.match.ParticipantStatsData

            # Determine stats of user whose match history this is
            for participant in match.participants:
                if participant.summoner.name == self.username:
                    team = participant.side.name
                    player = participant
                    player_stats = participant.stats

            # Cast and determine slightly more complex variables
            if match.is_remake:
                win = 'remake'
            else:
                win = 'win' if player.stats.win else 'loss'

            # Display the data in the game container
            key_data = Label(
                master=game, text='key: ' + str(key) + ', match: ' + str(match.id)
            )
            key_data.grid(row=0, column=0)

            outcome = Label(master=game, text=win)
            outcome.grid(row=1, column=0)

            champion_played = Label(master=game, text=player.champion.name)
            champion_played.grid(row=1, column=1)

            # Save each game to the grid
            game.grid(row=key, pady=10)

    def __del__(self):
        hinter.ui.main.UI.clear_screen()
