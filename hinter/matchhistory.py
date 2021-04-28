from tkinter import *
import tkinter
from PIL import ImageTk, Image
import datetime
import timeago
import pytz

import cassiopeia

import hinter
import hinter.struct.user
import hinter.ui.main


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
        champ_size = (64, 64)
        rune_size = (30, 30)
        sec_rune_size = (26, 26)
        spell_size = (30, 30)

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
            team_kills: int = 0

            # Determine stats of user whose match history this is
            for participant in match.participants:
                if participant.summoner.name == self.username:
                    team = participant.side.name
                    player = participant

            # Determine player's team's kill count
            for participant in match.participants:
                if participant.side.name == team:
                    team_kills += participant.stats.kills

            # Resolve ending condition of game
            if match.is_remake:
                win = 'Remake'
            else:
                win = 'Victory' if player.stats.win else 'Defeat'

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
                    runes_taken['secondary']['image'] = rune.path.image.resize(sec_rune_size)

                # Store list of actual runes used
                runes_taken['runes'].append(rune.name)

            '''Assign the data to widgets to be displayed'''
            # Upfront data, win and champ
            img = ImageTk.PhotoImage(image=player.champion.image.image.resize(champ_size))
            champion_played = Label(master=game, image=img)
            champion_played.image = img

            outcome = Label(master=game, text=win)

            match_length_parts = str(match.duration).split(':')
            match_minutes = int(match_length_parts[0] * 60)
            match_minutes += int(match_length_parts[1])
            match_minutes += (int(match_length_parts[2]) / 60)
            match_minutes = round(match_minutes, 2)

            now = datetime.datetime.utcnow()
            now = pytz.utc.localize(now)
            match_time = datetime.datetime.fromisoformat(
                str(match.creation)
            )
            duration = str(match.duration) + ' long - ' + timeago.format(match_time, now)

            timing = Label(master=game, text=duration)

            # Summoner Spells
            spell_d: cassiopeia.SummonerSpell = player.summoner_spell_d
            spell_f: cassiopeia.SummonerSpell = player.summoner_spell_f

            img = ImageTk.PhotoImage(image=spell_d.image.image.resize(spell_size))
            spell_d_used = Label(master=game, image=img)
            spell_d_used.image = img

            img = ImageTk.PhotoImage(image=spell_f.image.image.resize(spell_size))
            spell_f_used = Label(master=game, image=img)
            spell_f_used.image = img

            # Runes
            img = ImageTk.PhotoImage(image=runes_taken['key']['image'])
            key_rune_used = Label(master=game, image=img)
            key_rune_used.image = img

            img = ImageTk.PhotoImage(image=runes_taken['secondary']['image'])
            secondary_rune_used = Label(master=game, image=img)
            secondary_rune_used.image = img

            # Number data, kda, dmg, gold
            kills_assists = player.stats.kills + player.stats.assists
            kda = kills_assists
            if player.stats.deaths != 0:  # Avoid dividing my zero
                kda /= player.stats.deaths

            kda = round(kda, 2)  # Trim off excess decimal places

            kda_display = Label(master=game, text=str(kda) + ' KDA')
            k_d_a_display = Label(master=game, text=str(player.stats.kills) + ' / ' + str(player.stats.deaths) + ' / ' + str(player.stats.assists))

            kill_participation = int(round(kills_assists / team_kills * 100, 0))

            damage = Label(master=game, text=str(player.stats.total_damage_dealt_to_champions) + 'dmg')

            gold = Label(master=game, text=str(player.stats.gold_earned) + 'g')

            vision_min = round(player.stats.vision_score / match_minutes, 2)
            vision_min = Label(master=game, text=str(vision_min) + ' Vis/Min')

            vision = Label(master=game, text=str(player.stats.vision_score) + ' Vis - ' + str(kill_participation) + '% KP')

            '''Display and organize game widgets'''
            # First row - game type, win/loss, time-ago, duration
            outcome.grid(row=1, column=0, pady=5)
            timing.grid(row=1, column=5, columnspan=2)

            # Second row - champion, spells, runes, kda, cs/min, dmg/min, items
            champion_played.grid(row=2, column=0, rowspan=2)
            spell_d_used.grid(row=2, column=1)
            key_rune_used.grid(row=2, column=2)
            kda_display.grid(row=2, column=3)
            vision_min.grid(row=2, column=4, padx=15)

            # Third row - spells, runes, k/d/a, cs, dmg and %team, items
            spell_f_used.grid(row=3, column=1)
            secondary_rune_used.grid(row=3, column=2)
            kda_display.grid(row=3, column=3, padx=60)
            vision.grid(row=3, column=4, padx=60)

            #
            damage.grid(row=2, column=7)
            gold.grid(row=2, column=8)

            # Save each game to the grid
            game.grid(row=key, pady=10)

    def __del__(self):
        hinter.ui.main.UI.clear_screen()
