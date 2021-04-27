from tkinter import *

import cassiopeia

import hinter
import hinter.struct.user
import hinter.ui.main

from PIL import ImageTk, Image


class MatchHistory:
    games: cassiopeia.MatchHistory
    games_shown: int = 10
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

        # Load match history information
        self.games = user.match_history(end_index=200)

    def show_match_screen(self):
        hinter.ui.main.UI.clear_screen()
        hinter.ui.main.UI.new_screen()
        hinter.ui.main.UI.screen.grid(row=0, column=0, pady=20)

        # Set up the left-bar
        self.left_bar = Frame(master=hinter.ui.main.UI.screen)
        text = Label(master=self.left_bar, text='rank, icon, level, lp, users-played-with stats here')
        text.grid()
        self.left_bar.grid(row=0, column=0, padx=20, sticky=W)

        # Set up the right-bar
        self.right_bar = Frame(master=hinter.ui.main.UI.screen)
        text = Label(master=self.right_bar, text='role distribution, champ wr here')
        text.grid()
        self.right_bar.grid(row=0, column=2, padx=15, sticky=E)

        # Set up the main match history, and call to show all matches
        self.history = Frame(master=hinter.ui.main.UI.screen)

        self.display_matches()

        # Display match history
        self.history.grid(row=0, column=1, padx=15, sticky=N)

    def display_matches(self):
        # Have filler if the user is not in any games
        if not self.games:
            game = Frame(self.history)
            champion_played = Label(master=game, text='There are no games for this user, yet!')
            champion_played.grid(row=1, column=2)
            game.grid(row=0, pady=10)
            return

        # Loop through the first games
        for key, match in enumerate(self.games[0:self.games_shown]):
            # Set up each game's container, and cast multiple variables
            game = Frame(self.history)
            match: cassiopeia.Match
            team: str
            player: cassiopeia.core.match.Participant = cassiopeia.core.match.Participant()
            rune_size = (20,20)

            # Determine stats of user whose match history this is
            for participant in match.participants:
                if participant.summoner.name == self.username:
                    team = participant.side.name
                    player = participant
                    player_stats: cassiopeia.core.match.ParticipantStats = participant.stats

            # Resolve ending condition of game
            if match.is_remake:
                win = 'remake'
            else:
                win = 'win' if player.stats.win else 'loss'

            # Structure what runes the player took
            runes_taken = {
                'key': {
                    'name': str,
                    'image': Image,
                    'path': str,
                },
                'secondary': {
                    'name': str,
                    'image': str,
                },
                'runes': [],
            }

            # Resolve what runes the player took
            for trash, rune in enumerate(player.runes):
                rune: cassiopeia.Rune

                # Store keystone information
                if rune.is_keystone:
                    runes_taken['key']['name'] = rune.name
                    runes_taken['key']['image'] = rune.image.image.resize(rune_size)
                    runes_taken['key']['path'] = rune.path.name

                # Store secondary rune tree information
                if rune.path.name != runes_taken['key']['path']:
                    runes_taken['secondary']['name'] = rune.path.name
                    runes_taken['secondary']['image'] = rune.path.image_url

                # Store list of actual runes used
                runes_taken['runes'].append(rune.name)

            # Display the data in the game container
            outcome = Label(master=game, text=win + '(' + team + ')')
            outcome.grid(row=1, column=0)

            spells = Label(master=game, text=player.summoner_spell_d.name + ', ' + player.summoner_spell_f.name)
            spells.grid(row=1, column=1)

            champion_played = Label(master=game, text=player.champion.name + ' (' + str(player.stats.level) + ')')
            champion_played.grid(row=1, column=2)

            img = ImageTk.PhotoImage(image=runes_taken['key']['image'])

            runes_used = Label(master=game, image=img)
            runes_used.image = img
            runes_used.grid(row=1, column=3)

            kda_display = Label(master=game, text=str(player.stats.kills) + ' / ' + str(player.stats.deaths) + ' / ' + str(player.stats.assists))
            kda_display.grid(row=1, column=5)

            damage = Label(master=game, text=str(player.stats.total_damage_dealt_to_champions) + 'dmg')
            damage.grid(row=1, column=6)

            gold = Label(master=game, text=str(player.stats.gold_earned) + 'g')
            gold.grid(row=1, column=7)

            # Save each game to the grid
            game.grid(row=key, pady=10)

    def __del__(self):
        hinter.ui.main.UI.clear_screen()
