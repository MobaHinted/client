from tkinter import *
from PIL import ImageTk, Image
import datetime
import timeago
import timeago.locales.en   # Required for building to executable
import pytz

import cassiopeia

import hinter
import hinter.struct.user
import hinter.ui.main

import json


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
            user = cassiopeia.get_summoner(name=user.username, region=hinter.settings.region)
        else:
            user = cassiopeia.get_summoner(name=hinter.settings.active_user, region=hinter.settings.region)
        self.username = user.name

        # Save variables
        self.games = user.match_history
        self.rank = user.ranks[cassiopeia.Queue.ranked_solo_fives]
        self.level = user.level
        self.icon = user.profile_icon

        # Load match history information
        # self.games = user.match_history(count=200)

    def show_match_screen(self):
        hinter.ui.main.UI.clear_screen()
        hinter.ui.main.UI.new_screen()
        hinter.ui.main.UI.screen.grid(row=0, column=0, pady=20)

        # Set up the left-bar
        self.left_bar = Frame(master=hinter.ui.main.UI.screen)
        text = Label(master=self.left_bar, text='rank, icon, level, lp, users-played-with stats here')
        text.grid()
        self.left_bar.grid(row=0, column=0, padx=20, sticky=NW)

        # Set up the right-bar
        self.right_bar = Frame(master=hinter.ui.main.UI.screen)
        text = Label(master=self.right_bar, text='role distribution, champ wr here')
        text.grid()
        self.right_bar.grid(row=0, column=2, padx=15, sticky=NE)

        # Set up the main match history, and call to show all matches
        self.history = Frame(master=hinter.ui.main.UI.screen)

        self.display_matches()

        # Display match history
        self.history.grid(row=0, column=1, padx=15, sticky=N)

    def display_matches(self):
        champ_size = (64, 64)
        rune_size = (30, 30)
        sec_rune_size = (22, 22)
        spell_size = (30, 30)

        # Simplify Label creation
        def game_label(text: str = '', image: PhotoImage = None):
            if image is not None:
                returning = Label(master=game, image=image)
                returning.image = image
                return returning
            return Label(master=game, text=text)

        # Have filler if the user has not been in any games
        if not self.games:
            game = Frame(self.history)
            champion_played = game_label('There are no games for this user, yet!')
            champion_played.grid(row=1, column=2)
            game.grid(row=0, pady=10)
            return

        # Loop through the first games
        for key, match in enumerate(self.games[0:self.games_shown]):
            # Set up each game's container, and cast or setup multiple variables
            game = Frame(self.history)
            match: cassiopeia.Match
            team: str = '?'
            player: cassiopeia.core.match.Participant
            player = cassiopeia.core.match.Participant()
            player.stats: cassiopeia.core.match.ParticipantStats
            team_kills: int = 0
            team_damage: int = 0
            loss_color: str = '#DC9E9E'
            victory_color: str = '#97C79A'
            remake_color: str = 'grey94'
            background_color: str = remake_color

            # Determine type of game
            queue = match.queue.name
            if match.queue == cassiopeia.data.Queue.ranked_solo_fives:
                queue = 'Ranked Solo'
            elif match.queue == cassiopeia.data.Queue.ranked_flex_fives:
                queue = 'Ranked Flex'
            elif match.queue == cassiopeia.data.Queue.clash:
                queue = 'Clash'
            elif match.queue == cassiopeia.data.Queue.blind_fives:
                queue = 'Normal Blind'
            elif match.queue == cassiopeia.data.Queue.normal_draft_fives:
                queue = 'Normal Draft'
            elif match.queue == cassiopeia.data.Queue.aram:
                queue = 'ARAM'
            else:
                queue = queue.replace('_', ' ').title()

            # Determine stats of user whose match history this is
            for participant in match.participants:
                if participant.summoner.name == self.username:
                    team = participant.side.name
                    player = participant

            # Determine player's team's kill count
            for participant in match.participants:
                if participant.side.name == team:
                    team_kills += participant.stats.kills
                    team_damage += \
                        participant.stats.total_damage_dealt_to_champions

            # Resolve ending condition of game
            if match.is_remake:
                win = 'Remake'
            else:
                if player.stats.win:
                    win = 'Victory'
                    background_color = victory_color
                else:
                    win = 'Defeat'
                    background_color = loss_color

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
                    runes_taken['key']['image'] = rune.image.image.resize(
                        rune_size
                    )
                    runes_taken['key']['path'] = rune.path.name

                # Store secondary rune tree information
                if rune.path.name != runes_taken['key']['path']:
                    runes_taken['secondary']['name'] = rune.path.name
                    runes_taken['secondary']['image'] = rune.path.image.resize(
                        sec_rune_size
                    )

                # Store list of actual runes used
                runes_taken['runes'].append(rune.name)

            '''Assign the data to widgets to be displayed'''

            # Upfront data, win and champ
            img = ImageTk.PhotoImage(
                image=player.champion.image.image.resize(champ_size)
            )
            champion_played = game_label(image=img)

            outcome = game_label(text=win)

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
            duration = str(match.duration) + ' long - '
            duration += timeago.format(match_time, now)

            timing = game_label(text=duration)

            # Summoner Spells
            spell_d: cassiopeia.SummonerSpell = player.summoner_spell_d
            spell_f: cassiopeia.SummonerSpell = player.summoner_spell_f

            img = ImageTk.PhotoImage(
                image=spell_d.image.image.resize(spell_size)
            )
            spell_d_used = game_label(image=img)

            img = ImageTk.PhotoImage(
                image=spell_f.image.image.resize(spell_size)
            )
            spell_f_used = game_label(image=img)

            # Only check any lane/role data if this is summoner's rift
            if match.map.id == 11:
                # Determine role of player
                role = str(player.stats.role)
                lane = str(player.lane)
                position: cassiopeia.data.Position = cassiopeia.data.Position.none

                cassiopeia.core.Items(region=hinter.settings.region)

                # Search for support item
                has_support: bool = False
                support_items = [
                    3853,  # shard of true ice
                    3851,  # frostfang
                    3850,  # spellthief
                    3860,  # bulwark of the mountain
                    3859,  # targons buckler
                    3858,  # relic shield
                    3864,  # black mist scythe
                    3863,  # harrowing crescent
                    3862,  # spectral sickle
                    3857,  # pauldrons of whiterock
                    3855,  # runesteel spaulders
                    3854,  # steel shoulderguards
                ]
                for item in player.stats.items:
                    if item is None:
                        continue

                    if item.id in support_items:
                        has_support = True

                # Check spells
                has_smite: bool = False
                if spell_d.name == 'Smite' or spell_f.name == 'Smite':
                    has_smite = True
                has_teleport: bool = False
                if spell_d.name == 'Teleport' or spell_f.name == 'Teleport':
                    has_teleport = True
                has_heal: bool = False
                if spell_d.name == 'Heal' or spell_f.name == 'Heal':
                    has_heal = True

            # Assign role
                # First assign off of lane/position as provided
                if 'solo' in role.lower():
                    if 'mid' in lane:
                        position = cassiopeia.data.Position.middle
                    else:
                        position = cassiopeia.data.Position.top
                elif 'jungle' in lane:
                    position = cassiopeia.data.Position.jungle
                else:
                    if 'support' in role.lower():
                        position = cassiopeia.data.Position.utility
                    else:
                        position = cassiopeia.data.Position.bottom

                # Next assign if no assignment was made
                if position is cassiopeia.data.Position.none:
                    if has_support:
                        position = cassiopeia.data.Position.utility
                    elif has_smite:
                        position = cassiopeia.data.Position.jungle
                    elif has_heal:
                        position = cassiopeia.data.Position.bottom
                    elif 'mid' in lane:
                        position = cassiopeia.data.Position.mid
                    elif 'top' in lane:
                        position = cassiopeia.data.Position.top

            # Undo labelling if not on summoner's rift
            if match.map.id != 11:
                played_position = game_label('')
            # Change 'utility' to 'support'
            elif position == cassiopeia.data.Position.utility:
                played_position = game_label('Support')
            else:
                played_position = game_label(position.name.capitalize())

            # Runes
            img = ImageTk.PhotoImage(image=runes_taken['key']['image'])
            key_rune_used = game_label(image=img)

            img = ImageTk.PhotoImage(image=runes_taken['secondary']['image'])
            secondary_rune_used = game_label(image=img)

            # Number data, kda, dmg, gold
            kills_assists = player.stats.kills + player.stats.assists
            kda = kills_assists
            if player.stats.deaths != 0:  # Avoid dividing my zero
                kda /= player.stats.deaths
            kda = round(kda, 2)  # Trim off excess decimal places

            kda_display = game_label(text=str(kda) + ' KDA')
            k_d_a_display = game_label(
                str(player.stats.kills) + ' / ' + str(player.stats.deaths)
                + ' / ' + str(player.stats.assists)
            )

            kill_participation = kills_assists / (team_kills + 0.00000001) * 100
            kill_participation = int(round(kill_participation, 0))

            damage = player.stats.total_damage_dealt_to_champions
            damage_of_team = int(round(damage / (team_damage + 0.1) * 100, 0))
            damage_min = int(round(damage / match_minutes, 0))
            damage_min = game_label(text=str(damage_min) + ' DMG/Min')
            damage = game_label(
                str(damage) + ' DMG - ' + str(damage_of_team) + '%/Team'
            )

            vision_min = round(player.stats.vision_score / match_minutes, 2)
            vision_min = game_label(text=str(vision_min) + ' Vis/Min')

            vision = game_label(
                str(player.stats.vision_score) + ' Vis - '
                + str(kill_participation) + '% KP'
            )

            cs_gotten = player.stats.total_minions_killed
            cs_gotten += player.stats.neutral_minions_killed
            cs_min = round(cs_gotten / match_minutes, 1)
            cs_min = game_label(text=str(cs_min) + ' CS/Min')
            total_cs = game_label(text=str(cs_gotten) + ' CS')

            '''Display and organize game widgets'''

            # First row - game type, win/loss, time-ago, duration
            outcome.grid(row=1, column=0, pady=5)
            outcome.config(font=('*Font', 20), bg=background_color)
            played_position.grid(row=1, column=3)
            played_position.config(font=('*Font', 14), bg=background_color)
            queue_type = game_label(text=queue)
            queue_type.grid(row=1, column=4)
            queue_type.config(font=('*Font', 14), bg=background_color)
            timing.grid(row=1, column=5, columnspan=2, sticky=SE)
            timing.config(font=('*Font', 14), bg=background_color)

            # Second row - champion, spells, runes, kda, cs/min, dmg/min, items
            champion_played.grid(row=2, column=0, rowspan=2)
            champion_played.config(bg=background_color)
            spell_d_used.grid(row=2, column=1)
            spell_d_used.config(bg=background_color)
            key_rune_used.grid(row=2, column=2)
            key_rune_used.config(bg=background_color)
            kda_display.grid(row=2, column=3, padx=40)
            kda_display.config(bg=background_color)
            vision_min.grid(row=2, column=4)
            vision_min.config(bg=background_color)
            cs_min.grid(row=2, column=5, padx=40)
            cs_min.config(bg=background_color)
            damage_min.grid(row=2, column=6)
            damage_min.config(bg=background_color)

            # Third row - spells, runes, k/d/a, cs, dmg and %team, items
            spell_f_used.grid(row=3, column=1)
            spell_f_used.config(bg=background_color)
            secondary_rune_used.grid(row=3, column=2)
            secondary_rune_used.config(bg=background_color)
            k_d_a_display.grid(row=3, column=3)
            k_d_a_display.config(bg=background_color)
            vision.grid(row=3, column=4)
            vision.config(bg=background_color)
            total_cs.grid(row=3, column=5)
            total_cs.config(bg=background_color)
            damage.grid(row=3, column=6)
            damage.config(bg=background_color)

            # Color game based on win/loss
            game.config(bg=background_color)

            # Save each game to the grid
            game.grid(row=key, pady=10, sticky=W+E)

    def __del__(self):
        hinter.ui.main.UI.clear_screen()
