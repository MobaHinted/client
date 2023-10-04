import datetime
from typing import Union

import dearpygui.dearpygui

import cassiopeia
import pytz
import timeago
import timeago.locales.en  # Required for building to executable
from PIL import Image

import hinter
import hinter.struct.user


class MatchHistory:
    games: cassiopeia.MatchHistory
    games_shown: int = 50
    rank: cassiopeia.Rank
    average_kda: float
    level = 0
    icon = 0
    username = ""
    table: str = 'match_history_table'
    table_row: str = 'match_history_table-row'
    left_bar: str = 'match_history_table-left'
    history: str = 'match_history_table-history-container'
    right_bar: str = 'match_history_table-right'
    ui: hinter.ui.main.UI

    def __init__(self, ui: hinter.ui.main.UI, user: hinter.struct.user.User = None):
        # Load summoner information
        if user is not None:
            user = cassiopeia.get_summoner(name=user.username, region=hinter.settings.region)
        elif hinter.settings.active_user != '':
            user = cassiopeia.get_summoner(name=hinter.settings.active_user, region=hinter.settings.region)
        else:
            return

        self.ui = ui

        self.username = user.name

        # Try to load rank
        try:
            self.games = user.match_history
            if cassiopeia.Queue.ranked_solo_fives in user.ranks:
                self.rank = user.ranks[cassiopeia.Queue.ranked_solo_fives]
            elif cassiopeia.Queue.ranked_flex_fives in user.ranks:
                self.rank = user.ranks[cassiopeia.Queue.ranked_flex_fives]
            else:
                self.rank = None

        # Error out if that code doesn't work, which indicates an API issue
        except Exception as e:
            self.delete_previous_screens(delete_current=True)

            self.ui.imgui.set_viewport_min_width(350)
            self.ui.imgui.set_viewport_width(350)
            self.ui.imgui.set_viewport_min_height(600)
            self.ui.imgui.set_viewport_height(600)

            if '503' in str(e):
                region = cassiopeia.Region(hinter.settings.region)
                platform = cassiopeia.Platform[region.name].value.lower()

                with self.ui.imgui.window(tag='error'):
                    self.ui.imgui.add_spacer(height=150)

                    text = 'Riot services are unavailable.'
                    self.ui.imgui.add_text(f'{text:^40}')
                    text = 'Please try later.'
                    self.ui.imgui.add_text(f'{text:^40}')

                    self.ui.imgui.add_spacer(height=40)

                    text = 'You can check the LoL status page:'
                    self.ui.imgui.add_text(f'{text:^40}')
                    self.ui.imgui.add_button(
                        label='Open status.rito Page',
                        callback=lambda: webbrowser.open(f'https://status.riotgames.com/lol?region={platform}'),
                        width=-1,
                    )
                    text = '(rarely posted if issues are unexpected)'
                    self.ui.imgui.add_text(f'{text:^40}')

                self.ui.imgui.set_primary_window('error', True)
                self.ui.imgui.start_dearpygui()
                exit(503)
            elif '403' in str(e):
                with self.ui.imgui.window(tag='error'):
                    self.ui.imgui.add_spacer(height=175)
                    text = 'This API key is invalid or expired.'
                    self.ui.imgui.add_text(f'{text:^40}')
                    text = 'Please enter a new one.'
                    self.ui.imgui.add_text(f'{text:^40}')

                    self.ui.imgui.add_spacer(height=20)

                    text = 'You can get a new one here:'
                    self.ui.imgui.add_text(f'{text:^40}')
                    self.ui.imgui.add_button(
                        label='Open developer.rito Page',
                        callback=lambda: webbrowser.open('https://developer.riotgames.com'),
                        width=-1,
                    )

                self.ui.imgui.set_primary_window('error', True)
                self.ui.imgui.start_dearpygui()
                exit(403)
            else:
                print(e)
                exit('unknown error')

        self.level = user.level
        self.icon = user.profile_icon

        # Load match history information
        # self.games = user.match_history(count=50)
    def show_match_screen(self, render: bool = True):
        self.ui.new_screen(tag='match_history')

        # Set up the table
        self.ui.imgui.add_table(
            tag=self.table,
            header_row=False,
            parent='match_history',
        )
        self.ui.imgui.add_table_row(
            parent=self.table,
            tag=self.table_row,
        )

        # region Left Bar
        # Set up the left-bar
        self.ui.imgui.add_table_column(
            parent=self.table,
            tag=self.left_bar,
            init_width_or_weight=0.2,
        )
        with self.ui.imgui.table_cell(parent=self.table_row):
            with self.ui.imgui.table(header_row=False):
                self.ui.imgui.add_table_column()

                # User name, centered
                with self.ui.imgui.table_row():
                    with self.ui.imgui.table(header_row=False):
                        # Adjust widths to center username
                        #  at 40pt it can fit 17 characters, and max character length for names is 16
                        portion = 1.0 / 16
                        name_portion = portion * len(self.username)
                        spacer_portion = (1.0 - name_portion) / 2

                        self.ui.imgui.add_table_column(init_width_or_weight=spacer_portion)
                        self.ui.imgui.add_table_column(init_width_or_weight=name_portion)
                        self.ui.imgui.add_table_column(init_width_or_weight=spacer_portion)

                        # Center the username
                        with self.ui.imgui.table_row():
                            self.ui.imgui.add_spacer()

                            self.ui.imgui.add_text(self.username)
                            self.ui.imgui.bind_item_font(self.ui.imgui.last_item(), self.ui.font['40 bold'])

                            self.ui.imgui.add_spacer()

                # Rank
                # TODO: Master+ has no division, display LP/position?
                if self.rank is not None:
                    with self.ui.imgui.table_row():
                        with self.ui.imgui.table(header_row=False):
                            self.ui.imgui.add_table_column(init_width_or_weight=0.275)
                            self.ui.imgui.add_table_column(init_width_or_weight=0.45)
                            self.ui.imgui.add_table_column(init_width_or_weight=0.275)

                            with self.ui.imgui.table_row():
                                self.ui.imgui.add_spacer()

                                with self.ui.imgui.group(horizontal=True):
                                    # Show the icon
                                    rank_icon_texture = self.ui.load_image(
                                        'rank-' + self.rank.tier.name,
                                        self.ui.FILE,
                                        './data/ranked-emblem/emblem-' + self.rank.tier.name + '.png',
                                        (477, 214, 810, 472),
                                        (86, 60),
                                    )
                                    self.ui.imgui.add_image(texture_tag=rank_icon_texture)

                                    # Show the rank name
                                    rank_name = self.rank.division.value
                                    self.ui.imgui.add_text(rank_name)
                                    self.ui.imgui.bind_item_font(self.ui.imgui.last_item(), self.ui.font['56 bold'])

                                self.ui.imgui.add_spacer()

                with self.ui.imgui.table_row():
                    self.ui.imgui.add_text('level, lp, users-played-with stats here')
        # endregion Left Bar

        # region  Center (Match History container)
        # Set up the center column, just a container for match history
        self.ui.imgui.add_table_column(
            parent=self.table,
            init_width_or_weight=0.60,
        )
        # Add a table that matches can be added to as rows, everything else is just a placeholder until the matches load
        with self.ui.imgui.table_cell(parent=self.table_row):
            with self.ui.imgui.table(header_row=False, tag=self.history, pad_outerX=True):
                self.ui.imgui.add_table_column(tag='match-history-delete-5')
                self.ui.imgui.add_table_column()  # Actual destination for matches
                self.ui.imgui.add_table_column(tag='match-history-delete-6')

                with self.ui.imgui.table_row(tag='match-history-delete-1'):
                    self.ui.imgui.add_spacer(tag='match-history-delete-2')
                    self.ui.imgui.add_text(
                        'Loading Match History. Waiting for Rito...\n\nIf this is your first time seeing this:' +
                        '\nIt can take a couple minutes',
                        tag='match-history-delete-3',
                    )
                    self.ui.imgui.add_spacer(tag='match-history-delete-4')
        # endregion Center (Match History container)

        # region Right Bar
        # Set up the right-bar
        self.ui.imgui.add_table_column(
            parent=self.table,
            tag=self.right_bar,
            init_width_or_weight=0.2,
        )
        with self.ui.imgui.table_cell(parent=self.table_row):
            with self.ui.imgui.table(header_row=False):
                self.ui.imgui.add_table_column()

                with self.ui.imgui.table_row():
                    self.ui.imgui.add_text('role distribution, champ wr here')
        # endregion Right Bar

        # Display screen
        self.ui.imgui.set_viewport_min_width(1780)
        self.ui.imgui.set_viewport_width(1780)
        self.ui.imgui.set_viewport_min_height(670)
        self.ui.imgui.set_viewport_height(670)
        self.ui.new_screen(tag='match_history', set_primary=True)

        if render:
            self.ui.render_frames(60)
        else:
            self.ui.render_frames(60, split=True)

        # Load the user's match history
        self.display_matches()

    # noinspection DuplicatedCode
    def display_matches(self):
        champ_size = (64, 64)
        rune_size = (30, 30)
        sec_rune_size = (22, 22)
        spell_size = (30, 30)
        item_size = (30, 30)

        champ_icons = []

        # Have filler if the user has not been in any games
        if not self.games:
            with self.ui.imgui.table_row(parent=self.history):
                self.ui.imgui.add_spacer()
                self.ui.imgui.add_text('There are no games for this user, yet!')
                self.ui.imgui.add_spacer()
            return

        self.ui.imgui.delete_item(item='match-history-delete-1')
        self.ui.imgui.delete_item(item='match-history-delete-2')
        self.ui.imgui.delete_item(item='match-history-delete-3')
        self.ui.imgui.delete_item(item='match-history-delete-4')
        self.ui.imgui.delete_item(item='match-history-delete-5')
        self.ui.imgui.delete_item(item='match-history-delete-6')

        row_count = 0
        # Loop through the first games
        for key, match in enumerate(self.games[0:self.games_shown]):
            self.ui.render_frames()

            # Set up each game's container, and cast or setup multiple variables
            match: cassiopeia.Match
            team: str = '?'
            player: cassiopeia.core.match.Participant
            player = cassiopeia.core.match.Participant()
            player.stats: cassiopeia.core.match.ParticipantStats
            team_kills: int = 0
            team_damage: int = 0

            loss_color = [220, 158, 158, 40]
            victory_color = [151, 199, 154, 60]
            remake_color = [255, 255, 255, 10]
            background_color: str = remake_color
            filler = ''

            '''Resolve some data to work from'''

            # region Determine type of game
            queue = match.queue.name
            if match.queue == cassiopeia.data.Queue.ranked_solo_fives or \
                    match.queue == cassiopeia.data.Queue.ranked_solo_fives.name:
                queue = 'Ranked Solo'
            elif match.queue == cassiopeia.data.Queue.ranked_flex_fives or \
                    match.queue == cassiopeia.data.Queue.ranked_flex_fives.name:
                queue = 'Ranked Flex'
            elif match.queue == cassiopeia.data.Queue.clash or \
                    match.queue == cassiopeia.data.Queue.clash.name:
                queue = 'Clash'
            elif match.queue == cassiopeia.data.Queue.blind_fives or \
                    match.queue == cassiopeia.data.Queue.blind_fives.name:
                queue = 'Normal Blind'
            elif match.queue == cassiopeia.data.Queue.normal_draft_fives or \
                    match.queue == cassiopeia.data.Queue.normal_draft_fives.name:
                queue = 'Normal Draft'
            elif match.queue == cassiopeia.data.Queue.aram or \
                    match.queue == cassiopeia.data.Queue.aram.name:
                queue = 'ARAM'
            elif match.queue == cassiopeia.data.Queue.rings_of_wrath or \
                    match.queue == cassiopeia.data.Queue.rings_of_wrath.name:
                queue = 'Arena'
            else:
                queue = queue.replace('_', ' ').title()
            # endregion Determine type of game

            # region Determine stats of user whose match history this is
            for participant in match.participants:
                if participant.summoner.name == self.username:
                    team = participant.side.name
                    player = participant
            # endregion Determine stats of user whose match history this is

            # region Determine player's team's kill count
            for participant in match.participants:
                if participant.side.name == team:
                    team_kills += participant.stats.kills
                    team_damage += participant.stats.total_damage_dealt_to_champions
            # endregion Determine player's team's kill count

            # region Resolve ending condition of game
            if match.is_remake:
                win = 'Remake'
            else:
                if player.stats.win:
                    win = 'Victory'
                    background_color = victory_color
                else:
                    win = 'Defeat'
                    background_color = loss_color
            # endregion Resolve ending condition of game

            # region Runes Taken
            # Structure what runes the player took
            if queue != 'Arena':
                runes_taken = {
                    'key': {
                        'name': str,
                        'image': Union[Image.Image, str],
                        'path': str,
                    },
                    'secondary': {
                        'name': str,
                        'image': Union[Image.Image, str],
                    },
                    'runes': [],
                }

                # Resolve what runes the player took
                for trash, rune in enumerate(player.runes):
                    rune: cassiopeia.Rune

                    # Store keystone information
                    if rune.is_keystone:
                        runes_taken['key']['name'] = rune.name
                        runes_taken['key']['path'] = rune.path.name

                        if not self.ui.check_image_cache('rune-' + rune.name):
                            runes_taken['key']['image'] = rune.image.image
                        else:
                            runes_taken['key']['image'] = 'rune-' + rune.name

                    # Store secondary rune tree information
                    if rune.path.name != runes_taken['key']['path']:
                        runes_taken['secondary']['name'] = rune.path.name

                        if not self.ui.check_image_cache('rune-' + rune.path.name):
                            runes_taken['secondary']['image'] = rune.path.image
                        else:
                            runes_taken['secondary']['image'] = 'rune-' + rune.path.name

                    # Store list of actual runes used
                    runes_taken['runes'].append(rune.name)
            else:
                # TODO: Patch runes trying to be read in cassiopeia on arena modes
                runes_taken = {
                    'key': {
                        'name': 'na',
                        'image': 'na',
                        'path': 'na',
                    },
                    'secondary': {
                        'name': 'na',
                        'image': 'na',
                    },
                    'runes': [],
                }
            # endregion Runes Taken

            '''Calculate and format match data'''

            # Upfront data, win and champ
            if not self.ui.check_image_cache('champion-' + player.champion.name):
                champion_played = player.champion.image.image
            else:
                champion_played = 'champion-' + player.champion.name

            outcome = win

            # region Match Timing
            # Calculate match length in minutes
            match_length_parts = str(match.duration).split(':')
            match_minutes = int(match_length_parts[0] * 60)
            match_minutes += int(match_length_parts[1])
            match_minutes += (int(match_length_parts[2]) / 60)
            match_minutes = round(match_minutes, 2)

            # Calculate when the match happened
            now = datetime.datetime.utcnow()
            now = pytz.utc.localize(now)
            match_time = datetime.datetime.fromisoformat(
                str(match.creation)
            )

            # Format match timing and how long ago it was
            # duration = str(match.duration) + ' long - '  # HH:MM:SS display
            duration = f'{match_minutes:>2.0f}min - '
            duration += timeago.format(match_time, now)
            # endregion Match Timing

            # region Summoner Spells
            # Load the spells assigned to 'd' and 'f'
            spell_d: cassiopeia.SummonerSpell = player.summoner_spell_d
            spell_f: cassiopeia.SummonerSpell = player.summoner_spell_f

            # Save the images for each spell
            if not self.ui.check_image_cache('spell-' + spell_d.name):
                spell_d_used = spell_d.image.image
            else:
                spell_d_used = 'spell-' + spell_d.name
            if not self.ui.check_image_cache('spell-' + spell_f.name):
                spell_f_used = spell_f.image.image
            else:
                spell_f_used = 'spell-' + spell_f.name
            # endregion Summoner Spells

            # region Role
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
                        position = cassiopeia.data.Position.middle
                    elif 'top' in lane:
                        position = cassiopeia.data.Position.top

            # Undo labelling if not on summoner's rift
            if match.map.id != 11:
                played_position = ''
            # Change 'utility' to 'support'
            elif position == cassiopeia.data.Position.utility:
                played_position = 'Support'
            else:
                played_position = position.name.capitalize()
            # endregion Role

            # region Runes
            # Load the keystone rune
            key_rune_used = runes_taken['key']['image']

            # Load the secondary rune tree
            secondary_rune_used = runes_taken['secondary']['image']
            # endregion Runes

            # region KDA and KP
            # Calculate KDA
            kills_assists = player.stats.kills + player.stats.assists
            kda = kills_assists
            if player.stats.deaths != 0:  # Avoid dividing my zero
                kda /= player.stats.deaths
            kda = round(kda, 2)  # Trim off excess decimal places

            kda_display = f'{kda:.1f} KDA'
            k_d_a_display = (str(player.stats.kills) + ' / ' + str(player.stats.deaths) +
                             ' / ' + str(player.stats.assists))

            # Calculate KP
            kill_participation = kills_assists / (team_kills + 0.00000001) * 100
            kill_participation = int(round(kill_participation, 0))
            # endregion KDA and KP

            # region Damage
            damage = player.stats.total_damage_dealt_to_champions
            damage_of_team = int(round(damage / (team_damage + 0.1) * 100, 0))
            damage_min = int(round(damage / match_minutes, 0))
            damage_min = f'{damage_min:,} DMG/Min'
            if queue != 'Arena':
                damage = f'{damage:,} DMG - {damage_of_team}%'
            else:
                damage = f'{damage:,} DMG'
            # endregion Damage

            # region Vision
            # Calculate Vision/Min
            vision_min = round(player.stats.vision_score / match_minutes, 2)
            vision_min = str(vision_min) + ' Vis/Min'

            # Show vision score and kill participation
            vision = (str(player.stats.vision_score) + ' Vis - ' +
                      str(kill_participation) + '% KP')
            # endregion Vision

            # region Creep Score (CS) stats
            cs_gotten = player.stats.total_minions_killed
            cs_gotten += player.stats.neutral_minions_killed
            cs_min = round(cs_gotten / match_minutes, 1)
            cs_min = str(cs_min) + ' CS/Min'
            total_cs = f'{cs_gotten:,} CS'
            # endregion Creep Score (CS) stats

            # region Items
            items = []

            trinket = {
                'item': 'filler',
                'image': None,
            }
            trinkets = [
                3340,  # Warding Totem
                3363,  # Farsight Alteration
                3364,  # Oracle Lens
            ]

            # Arrange player items into a list, item id and the image
            for item in player.stats.items:
                if item is None:
                    items.append(
                        {
                            'item': 'filler',
                            'image': None,
                        }
                    )
                    continue

                if item.id in trinkets:
                    if not self.ui.check_image_cache(f'item-{item.id}'):
                        trinket = {
                            'item': item.id,
                            'image': item.image.image,
                        }
                    else:
                        trinket = {
                            'item': item.id,
                            'image': f'item-{item.id}',
                        }
                    continue

                if not self.ui.check_image_cache(f'item-{item.id}'):
                    items.append(
                        {
                            'item': item.id,
                            'image': item.image.image,
                        }
                    )
                else:
                    items.append(
                        {
                            'item': item.id,
                            'image': f'item-{item.id}',
                        }
                    )

            items.append(trinket)
            # endregion Items

            '''Display and organize game widgets'''

            counter = 0
            with self.ui.imgui.table_row(parent=self.history, tag=f'match-{match.id}'):
                with self.ui.imgui.table(header_row=False, no_clip=True):
                    self.ui.imgui.add_table_column()  # Outcome, champ played, spells, runes
                    self.ui.imgui.add_table_column()  # Lane, items
                    self.ui.imgui.add_table_column()  # Game Type, kda
                    self.ui.imgui.add_table_column()  # Vision, kp
                    self.ui.imgui.add_table_column()  # CS
                    self.ui.imgui.add_table_column()  # Match duration info, dmg

                    # region Row 1: Outcome, Lane, Game Type, Match duration info
                    with self.ui.imgui.table_row():
                        self.ui.imgui.add_text(outcome)
                        self.ui.imgui.bind_item_font(self.ui.imgui.last_item(), self.ui.font['24 regular'])

                        self.ui.imgui.add_text(played_position)

                        self.ui.imgui.add_text(f'{queue:^15}')

                        self.ui.imgui.add_spacer()
                        self.ui.imgui.add_spacer()

                        self.ui.imgui.add_text(f'{duration:>20}')
                    # endregion Row 1: Outcome, Lane, Game Type, Match duration info

                    # region Row 2: Champion, Spell, Key Rune, Items, KDA, Vision, CS, Damage
                    with self.ui.imgui.table_row(height=rune_size[1]):
                        with self.ui.imgui.group(horizontal=True):
                            if not self.ui.check_image_cache('champion-' + player.champion.name):
                                champion_played = self.ui.load_image(
                                    'champion-' + player.champion.name, self.ui.PIL, champion_played, size=champ_size
                                )
                            else:
                                champion_played = self.ui.load_image(champion_played, size=champ_size)

                            # Place a filler image for the champion icon (hack to span 2 rows)
                            self.ui.imgui.add_image(
                                texture_tag='CACHED_IMAGE-filler',
                                width=champ_size[0],
                                height=rune_size[1],
                                tag=f'champ-icon-holder-{match.id}',
                            )
                            # Draw a frame
                            self.ui.render_frames()

                            champ_icons.append(f'champ-icon-{match.id}')
                            # Place the champion icon over the filler image
                            self.ui.imgui.add_image(
                                texture_tag=champion_played,
                                tag=f'champ-icon-{match.id}',
                                parent='match_history',
                                pos=self.ui.imgui.get_item_pos(f'champ-icon-holder-{match.id}')
                            )

                            if not self.ui.check_image_cache('spell-' + spell_d.name):
                                spell_d_used = self.ui.load_image(
                                    'spell-' + spell_d.name, self.ui.PIL, spell_d_used, size=spell_size
                                )
                            else:
                                spell_d_used = self.ui.load_image(spell_d_used, size=spell_size)
                            self.ui.imgui.add_image(texture_tag=spell_d_used)

                            if queue == 'Arena':
                                self.ui.imgui.add_image(
                                    texture_tag='CACHED_IMAGE-filler',
                                    width=rune_size[0],
                                    height=rune_size[1],
                                )
                            elif not self.ui.check_image_cache(f'rune-{runes_taken["key"]["name"]}'):
                                key_rune_used = self.ui.load_image(
                                    'rune-' + runes_taken['key']['name'], self.ui.PIL, key_rune_used, size=rune_size
                                )
                                self.ui.imgui.add_image(texture_tag=key_rune_used)
                            else:
                                key_rune_used = self.ui.load_image(runes_taken['key']['image'], size=rune_size)
                                self.ui.imgui.add_image(texture_tag=key_rune_used)

                        # Show the first 3 items
                        with self.ui.imgui.group(horizontal=True):
                            for item in items:
                                if counter < 3:
                                    # Load the image if it is not a placeholder
                                    if item['item'] != 'filler':
                                        if not self.ui.check_image_cache(f'item-{item["item"]}'):
                                            image = self.ui.load_image(
                                                'item-' + str(item['item']), self.ui.PIL, item['image'], size=item_size
                                            )
                                        else:
                                            image = self.ui.load_image(f'item-{item["item"]}', size=item_size)
                                        self.ui.imgui.add_image(texture_tag=image)
                                    # Handle cases where there are <3 items
                                    else:
                                        self.ui.imgui.add_image(
                                            texture_tag='CACHED_IMAGE-filler',
                                            width=item_size[0],
                                            height=item_size[1],
                                        )
                                else:
                                    continue
                                counter += 1
                            # Filler '4th item' in this row to show above trinket
                            self.ui.imgui.add_image(
                                texture_tag='CACHED_IMAGE-filler',
                                width=item_size[0],
                                height=item_size[1],
                            )

                        self.ui.imgui.add_text(f'{kda_display:^15}')

                        if match.map.id != 11:
                            vision_min = filler
                        self.ui.imgui.add_text(f'{vision_min:^20}')

                        self.ui.imgui.add_text(f'{cs_min:^15}')

                        self.ui.imgui.add_text(f'{damage_min:^20}')
                    # endregion Row 2: Champion, Spell, Key Rune, Items, KDA, Vision, CS, Damage

                    # region Row 3: Spell, Sub Rune, Items, KDA, Vision/KP, CS, Damage
                    with self.ui.imgui.table_row():
                        with self.ui.imgui.group(horizontal=True):
                            self.ui.imgui.add_spacer(width=champ_size[0])

                            if not self.ui.check_image_cache('spell-' + spell_f.name):
                                spell_f_used = self.ui.load_image(
                                    'spell-' + spell_f.name, self.ui.PIL, spell_f_used, size=spell_size
                                )
                            else:
                                spell_f_used = self.ui.load_image(spell_f_used, size=spell_size)
                            self.ui.imgui.add_image(texture_tag=spell_f_used)

                            if queue == 'Arena':
                                self.ui.imgui.add_image(
                                    texture_tag='CACHED_IMAGE-filler',
                                    width=rune_size[0],
                                    height=rune_size[1],
                                )
                            elif not self.ui.check_image_cache(f'rune-{runes_taken["secondary"]["name"]}'):
                                secondary_rune_used = self.ui.load_image(
                                    'rune-' + runes_taken['secondary']['name'],
                                    self.ui.PIL,
                                    secondary_rune_used,
                                    size=rune_size,
                                )
                                self.ui.imgui.add_image(texture_tag=secondary_rune_used)
                            else:
                                secondary_rune_used = self.ui.load_image(
                                    f'rune-{runes_taken["secondary"]["name"]}',
                                    size=rune_size,
                                )
                                self.ui.imgui.add_image(texture_tag=secondary_rune_used)

                        # Show the last 3 items, and the trinket
                        counter = 0
                        with self.ui.imgui.group(horizontal=True):
                            for item in items:
                                # Skip the first 3 items
                                if counter >= 3:
                                    # Load the image if it is not a placeholder
                                    if item['item'] != 'filler':
                                        if not self.ui.check_image_cache(f'item-{item["item"]}'):
                                            image = self.ui.load_image(
                                                'item-' + str(item['item']), self.ui.PIL, item['image'], size=item_size
                                            )
                                        else:
                                            image = self.ui.load_image(f'item-{item["item"]}', size=item_size)
                                        self.ui.imgui.add_image(texture_tag=image)
                                    # Handle cases where there are <3 items
                                    else:
                                        self.ui.imgui.add_image(
                                            texture_tag='CACHED_IMAGE-filler',
                                            width=item_size[0],
                                            height=item_size[1],
                                        )
                                # Just iterate to the 4th item
                                else:
                                    counter += 1

                        self.ui.imgui.add_text(f'{k_d_a_display:^15}')

                        if match.map.id != 11:
                            vision = filler
                        self.ui.imgui.add_text(f'{vision:^20}')

                        self.ui.imgui.add_text(f'{total_cs:^15}')

                        self.ui.imgui.add_text(f'{damage:^20}')
                    # endregion Row 3: Spell, Sub Rune, Items, KDA, Vision/KP, CS, Damage

                    with self.ui.imgui.table_row():
                        self.ui.imgui.add_spacer(height=5)

            self.ui.imgui.set_table_row_color(
                table=self.history,
                row=row_count,
                color=background_color,
            )
            row_count += 1

        # region Workaround for multi-row-spanning champion image
        # Once match data is visible, add the champion image
        def resize_call(sender):
            # Get the match id
            match_id = sender.split('-')[-1]

            # Add the image
            self.ui.imgui.add_image(
                texture_tag=champ_icons[match_id],
                tag='champ-icon-' + match_id,
                parent='match_history',
                pos=self.ui.imgui.get_item_pos('champ-icon-holder-' + match_id)
            )

            # Delete the visibility handler
            self.ui.imgui.delete_item(item=sender)

        # Add a handler for when match data is visible, so we can get the position at that time
        #for icon in champ_icons:
        #    with self.ui.imgui.item_handler_registry():
        #        self.ui.imgui.add_item_visible_handler(callback=resize_call, tag=icon)
        #    self.ui.imgui.bind_item_handler_registry('champ-icon-ref-' + icon, self.ui.imgui.last_container())

        # TODO: Add a self.history resize handler that doesn't get removed, and adjusts the image position
        # endregion Workaround for multi-row-spanning champion image

    def delete_previous_screens(self, delete_history: bool = False, delete_current: bool = False):
        if self.ui.imgui.does_item_exist('login'):
            self.ui.imgui.delete_item('login')

        if self.ui.imgui.does_item_exist('loading'):
            self.ui.imgui.delete_item('loading')

        if delete_history:
            if self.ui.imgui.does_item_exist('match_history'):
                self.ui.imgui.delete_item('match_history')

        if delete_current:
            if self.ui.imgui.does_item_exist(self.ui.screen):
                self.ui.imgui.delete_item(self.ui.screen)

    def __del__(self):
        self.ui.clear_screen()
