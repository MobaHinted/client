import datetime
import webbrowser
from typing import Union

import cassiopeia
import pytz
import timeago
import timeago.locales.en  # Required for building to executable
from PIL import Image, ImageOps
import dearpygui.dearpygui

import hinter


class MatchHistory:
    # TODO: Make sure all of these are being filled in __init__
    games: cassiopeia.MatchHistory
    rank: Union[cassiopeia.Rank, None]
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
    imgui: dearpygui.dearpygui = dearpygui.dearpygui
    SUMMONERS_RIFT = 11
    players_played_with: hinter.PlayersPlayedWith = hinter.PlayersPlayedWith.PlayersPlayedWith()
    lanes_played = {}
    champions_played = {}

    def __init__(self, ui: hinter.ui.main.UI, user: hinter.User = None):
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
            # TODO: fix this in cassiopeia to get fewer calls on initial load
            # self.games = user.match_history(continent=user.region.continent, puuid=user.puuid, count=100)

            if cassiopeia.Queue.ranked_solo_fives in user.ranks:
                self.rank = user.ranks[cassiopeia.Queue.ranked_solo_fives]
            elif cassiopeia.Queue.ranked_flex_fives in user.ranks:
                self.rank = user.ranks[cassiopeia.Queue.ranked_flex_fives]
            else:
                self.rank = None

        # Error out if that code doesn't work, which indicates an API issue
        except Exception as e:
            self.delete_previous_screens(delete_current=True)

            self.imgui.set_viewport_min_width(350)
            self.imgui.set_viewport_width(350)
            self.imgui.set_viewport_min_height(600)
            self.imgui.set_viewport_height(600)

            if '503' in str(e):
                region = cassiopeia.Region(hinter.settings.region)
                platform = cassiopeia.Platform[region.name].value.lower()

                with self.imgui.window(tag='error'):
                    self.imgui.add_spacer(height=150)

                    text = 'Riot services are unavailable.'
                    self.imgui.add_text(f'{text:^40}')
                    text = 'Please try later.'
                    self.imgui.add_text(f'{text:^40}')

                    self.imgui.add_spacer(height=40)

                    text = 'You can check the LoL status page:'
                    self.imgui.add_text(f'{text:^40}')
                    self.imgui.add_button(
                        label='Open status.rito Page',
                        callback=lambda: webbrowser.open(f'https://status.riotgames.com/lol?region={platform}'),
                        width=-1,
                    )
                    text = '(rarely posted if issues are unexpected)'
                    self.imgui.add_text(f'{text:^40}')

                self.imgui.set_primary_window('error', True)
                self.imgui.start_dearpygui()
                self.ui.exit_callback()
                exit(503)
            elif '403' in str(e):
                with self.imgui.window(tag='error'):
                    self.imgui.add_spacer(height=175)
                    text = 'This API key is invalid or expired.'
                    self.imgui.add_text(f'{text:^40}')
                    text = 'Please enter a new one.'
                    self.imgui.add_text(f'{text:^40}')

                    self.imgui.add_spacer(height=20)

                    text = 'You can get a new one here:'
                    self.imgui.add_text(f'{text:^40}')
                    self.imgui.add_button(
                        label='Open developer.rito Page',
                        callback=lambda: webbrowser.open('https://developer.riotgames.com'),
                        width=-1,
                    )

                self.imgui.set_primary_window('error', True)
                self.imgui.start_dearpygui()
                self.ui.exit_callback()
                exit(403)
            else:
                print(e)
                exit('unknown error')

        self.level = user.level
        self.icon = user.profile_icon

    def show_match_screen(self, render: bool = True):
        self.delete_previous_screens()
        self.ui.new_screen(tag='match_history')

        # Set up the table
        self.imgui.add_table(
            tag=self.table,
            header_row=False,
            parent='match_history',
        )
        self.imgui.add_table_row(
            parent=self.table,
            tag=self.table_row,
        )

        # region Left Bar
        # Set up the left-bar
        self.imgui.add_table_column(
            parent=self.table,
            tag=self.left_bar,
            init_width_or_weight=0.2,
        )
        with self.imgui.table_cell(parent=self.table_row):
            with self.imgui.table(header_row=False, tag='match_history-friends-parent'):
                self.imgui.add_table_column()

                # User name, centered
                with self.imgui.table_row():
                    with self.imgui.table(header_row=False):
                        # Adjust widths to center username
                        #  at 40pt it can fit 17 characters, and max character length for names is 16
                        portion = 1.0 / 16
                        name_portion = portion * len(self.username)
                        spacer_portion = (1.0 - name_portion) / 2

                        self.imgui.add_table_column(init_width_or_weight=spacer_portion)
                        self.imgui.add_table_column(init_width_or_weight=name_portion)
                        self.imgui.add_table_column(init_width_or_weight=spacer_portion)

                        # Center the username
                        with self.imgui.table_row():
                            self.imgui.add_spacer()

                            self.imgui.add_text(self.username)
                            self.imgui.bind_item_font(self.imgui.last_item(), self.ui.font['40 bold'])

                            self.imgui.add_spacer()

                # Icon and level
                with self.imgui.table_row():
                    with self.imgui.table(header_row=False):
                        self.imgui.add_table_column(init_width_or_weight=0.2)
                        self.imgui.add_table_column(init_width_or_weight=0.6)
                        self.imgui.add_table_column(init_width_or_weight=0.2)

                        with self.imgui.table_row():
                            self.imgui.add_spacer()

                            with self.imgui.group(horizontal=True):
                                icon_name = f'summoner_icon-{self.icon.id}'

                                # TODO: Make a UI method from this
                                if not self.ui.check_image_cache(icon_name):
                                    mask = Image.open('./assets/circular_mask.png').convert('L')
                                    icon = ImageOps.fit(self.icon.image, mask.size, centering=(0.5, 0.5))
                                    icon.putalpha(mask)
                                    icon.save(f'./data/image_cache/{icon_name}.png')

                                summoner_icon_texture = self.ui.load_image(
                                    icon_name,
                                    size=(35, 35),
                                )

                                # Show the icon
                                self.imgui.add_image(texture_tag=summoner_icon_texture, tag='summoner_icon')

                                # Show the rank name
                                self.imgui.add_text(f'Level {self.level}')
                                self.imgui.bind_item_font(self.imgui.last_item(), self.ui.font['32 bold'])

                            self.imgui.add_spacer()

                # Rank
                # TODO: Master+ has no division, display LP/position?
                if self.rank is not None and hinter.settings.show_my_rank:
                    with self.imgui.table_row():
                        with self.imgui.group():
                            self.imgui.add_spacer(height=20)
                            with self.imgui.table(header_row=False):
                                self.imgui.add_table_column(init_width_or_weight=0.275)
                                self.imgui.add_table_column(init_width_or_weight=0.45)
                                self.imgui.add_table_column(init_width_or_weight=0.275)

                                with self.imgui.table_row():
                                    self.imgui.add_spacer()

                                    with self.imgui.group(horizontal=True):
                                        # Show the icon
                                        rank_icon_texture = self.ui.load_image(
                                            'rank-' + self.rank.tier.name,
                                            self.ui.FILE,
                                            './data/ranked-emblem/emblem-' + self.rank.tier.name + '.png',
                                            (477, 214, 810, 472),
                                            (86, 60),
                                        )
                                        self.imgui.add_image(texture_tag=rank_icon_texture)

                                        # Show the rank name
                                        rank_name = self.rank.division.value
                                        self.imgui.add_text(rank_name)
                                        self.imgui.bind_item_font(self.imgui.last_item(), self.ui.font['56 bold'])

                                    self.imgui.add_spacer()

                with self.imgui.table_row(tag='match_history-friends-ref'):
                    self.imgui.add_spacer()
        # endregion Left Bar

        # region  Center (Match History container)
        # Set up the center column, just a container for match history
        self.imgui.add_table_column(
            parent=self.table,
            init_width_or_weight=0.60,
        )
        # Add a table that matches can be added to as rows, everything else is just a placeholder until the matches load
        with self.imgui.table_cell(parent=self.table_row):
            with self.imgui.table(header_row=False, tag=self.history, pad_outerX=True):
                self.imgui.add_table_column(tag='match-history-delete-5')
                self.imgui.add_table_column()  # Actual destination for matches
                self.imgui.add_table_column(tag='match-history-delete-6')

                with self.imgui.table_row(tag='match-history-delete-1'):
                    self.imgui.add_spacer(tag='match-history-delete-2')
                    self.imgui.add_text(
                        'Loading Match History. Waiting for Rito...\n\nIf this is your first time seeing this:' +
                        '\nIt can take a couple minutes',
                        tag='match-history-delete-3',
                    )
                    self.imgui.add_spacer(tag='match-history-delete-4')
        # endregion Center (Match History container)

        # region Right Bar
        # Set up the right-bar
        self.imgui.add_table_column(
            parent=self.table,
            tag=self.right_bar,
            init_width_or_weight=0.2,
        )
        with self.imgui.table_cell(parent=self.table_row):
            with self.imgui.table(header_row=False):
                self.imgui.add_table_column()

                with self.imgui.table_row():
                    self.imgui.add_text('role distribution, champ wr here')
        # endregion Right Bar

        # Display screen
        self.imgui.set_viewport_min_width(hinter.settings.default_width)
        self.imgui.set_viewport_width(hinter.settings.width)
        self.imgui.set_viewport_min_height(hinter.settings.default_height)
        self.imgui.set_viewport_height(hinter.settings.height)
        self.ui.new_screen(tag='match_history', set_primary=True)

        self.ui.render_frames(60, split=not render)

        # Load the user's match history
        self.display_matches(render)

    # noinspection DuplicatedCode
    def display_matches(self, render: bool = True):
        champ_size = (64, 64)
        rune_size = (30, 30)
        sec_rune_size = (22, 22)
        spell_size = (30, 30)
        item_size = (30, 30)

        champ_icons = []

        # Have filler if the user has not been in any games
        if not self.games:
            with self.imgui.table_row(parent=self.history):
                self.imgui.add_spacer()
                self.imgui.add_text('There are no games for this user, yet!')
                self.imgui.add_spacer()
            return

        # region Remove loading info
        self.imgui.delete_item(item='match-history-delete-1')
        self.imgui.delete_item(item='match-history-delete-2')
        self.imgui.delete_item(item='match-history-delete-3')
        self.imgui.delete_item(item='match-history-delete-4')
        self.imgui.delete_item(item='match-history-delete-5')
        self.imgui.delete_item(item='match-history-delete-6')
        # endregion Remove loading info

        row_count = 0
        # Loop through the first games
        # noinspection PyTypeChecker
        for key, match in enumerate(self.games[0:hinter.settings.match_history_count]):
            self.ui.render_frames(render)

            # region Cast or setup multiple variables
            match: cassiopeia.Match
            team: str = '?'
            player: cassiopeia.core.match.Participant
            player = cassiopeia.core.match.Participant()
            # player.stats: cassiopeia.core.match.ParticipantStats
            team_kills: int = 0
            team_damage: int = 0

            loss_color = [220, 158, 158, 40]
            victory_color = [151, 199, 154, 60]
            remake_color = [255, 255, 255, 10]
            background_color = remake_color
            filler = ''
            # endregion Cast or setup multiple variables

            '''Resolve some data to work from'''

            # region Determine type of game
            # Handle old matches that can't be loaded
            # noinspection PyBroadException
            try:
                queue = match.queue.name
            except Exception:
                continue

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

            outcome = win
            # endregion Resolve ending condition of game

            self.track_champions(
                player.champion.name,
                outcome
            )

            # Track players played with
            for participant in match.participants:
                if participant.summoner.name != self.username:
                    self.players_played_with.add(
                        participant,
                        outcome,
                        participant.side.name == team
                    )

            # region Determine player's team's kill count
            for participant in match.participants:
                if participant.side.name == team:
                    team_kills += participant.stats.kills
                    team_damage += participant.stats.total_damage_dealt_to_champions
            # endregion Determine player's team's kill count

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
                for _, rune in enumerate(player.runes):
                    rune: cassiopeia.Rune

                    # Store keystone information
                    if rune.is_keystone:
                        # noinspection PyTypedDict
                        runes_taken['key']['name'] = rune.name
                        runes_taken['key']['path'] = rune.path.name

                        if not self.ui.check_image_cache('rune-' + rune.name):
                            runes_taken['key']['image'] = rune.image.image
                        else:
                            # noinspection PyTypedDict
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
            duration = duration.replace('utes', '')
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
            position: cassiopeia.data.Position = cassiopeia.data.Position.none
            if match.map.id == self.SUMMONERS_RIFT:
                # Determine role of player
                role = str(player.stats.role)
                lane = str(player.lane)

                cassiopeia.core.Items(region=hinter.settings.region)

                # Search for support item
                has_support: bool = False
                # noinspection SpellCheckingInspection
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
                    elif 'top' in lane or has_teleport:
                        position = cassiopeia.data.Position.top

            # Undo labelling if not on summoner's rift
            if match.map.id != self.SUMMONERS_RIFT:
                played_position = ''
            # Change 'utility' to 'support'
            elif position == cassiopeia.data.Position.utility:
                played_position = 'Support'
            else:
                played_position = position.name.capitalize()

            if match.map.id == self.SUMMONERS_RIFT:
                self.track_lanes(
                    played_position,
                    outcome
                )
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
            self.imgui.add_table_row(parent=self.history, tag=f'match-{match.id}')

            with self.imgui.table(parent=f'match-{match.id}', header_row=False, no_clip=True):
                # region Columns
                self.imgui.add_table_column()  # Outcome, champ played, spells, runes
                self.imgui.add_table_column()  # Lane, items
                self.imgui.add_table_column()  # Game Type, kda
                self.imgui.add_table_column()  # Vision, kp
                self.imgui.add_table_column()  # CS
                self.imgui.add_table_column()  # Match duration info, dmg
                # endregion Columns

                # region Row 1: Outcome, Lane, Game Type, Match duration info
                with self.imgui.table_row():
                    self.imgui.add_text(outcome)
                    self.imgui.bind_item_font(self.imgui.last_item(), self.ui.font['24 regular'])

                    self.imgui.add_text(played_position)

                    self.imgui.add_text(f'{queue:^15}')

                    self.imgui.add_spacer()
                    self.imgui.add_spacer()

                    self.imgui.add_text(f'{duration:>20}')
                # endregion Row 1: Outcome, Lane, Game Type, Match duration info

                # region Row 2: Champion, Spell, Key Rune, Items, KDA, Vision, CS, Damage
                with self.imgui.table_row(height=rune_size[1]):
                    with self.imgui.group(horizontal=True):
                        if not self.ui.check_image_cache('champion-' + player.champion.name):
                            champion_played = self.ui.load_image(
                                'champion-' + player.champion.name, self.ui.PIL, champion_played, size=champ_size
                            )
                        else:
                            champion_played = self.ui.load_image(champion_played, size=champ_size)

                        # Place a filler image for the champion icon (hack to span 2 rows)
                        self.imgui.add_image(
                            texture_tag='CACHED_IMAGE-filler',
                            width=champ_size[0],
                            height=rune_size[1],
                            tag=f'champ-icon-holder-{match.id}',
                        )
                        # Draw a frame
                        self.ui.render_frames(render)

                        champ_icons.append(f'champ-icon-{match.id}')
                        # Place the champion icon over the filler image
                        self.imgui.add_image(
                            texture_tag=champion_played,
                            tag=f'champ-icon-{match.id}',
                            parent='match_history',
                            pos=self.imgui.get_item_pos(f'champ-icon-holder-{match.id}')
                        )

                        if not self.ui.check_image_cache('spell-' + spell_d.name):
                            spell_d_used = self.ui.load_image(
                                'spell-' + spell_d.name, self.ui.PIL, spell_d_used, size=spell_size
                            )
                        else:
                            spell_d_used = self.ui.load_image(spell_d_used, size=spell_size)
                        self.imgui.add_image(texture_tag=spell_d_used)

                        if queue == 'Arena':
                            self.imgui.add_image(
                                texture_tag='CACHED_IMAGE-filler',
                                width=rune_size[0],
                                height=rune_size[1],
                            )
                        elif not self.ui.check_image_cache(f'rune-{runes_taken["key"]["name"]}'):
                            key_rune_used = self.ui.load_image(
                                'rune-' + runes_taken['key']['name'], self.ui.PIL, key_rune_used, size=rune_size
                            )
                            self.imgui.add_image(texture_tag=key_rune_used)
                        else:
                            key_rune_used = self.ui.load_image(runes_taken['key']['image'], size=rune_size)
                            self.imgui.add_image(texture_tag=key_rune_used)

                    # Show the first 3 items
                    with self.imgui.group(horizontal=True):
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
                                    self.imgui.add_image(texture_tag=image)
                                # Handle cases where there are <3 items
                                else:
                                    self.imgui.add_image(
                                        texture_tag='CACHED_IMAGE-filler',
                                        width=item_size[0],
                                        height=item_size[1],
                                    )
                            else:
                                continue
                            counter += 1
                        # Filler '4th item' in this row to show above trinket
                        self.imgui.add_image(
                            texture_tag='CACHED_IMAGE-filler',
                            width=item_size[0],
                            height=item_size[1],
                        )

                    self.imgui.add_text(f'{kda_display:^15}')

                    if match.map.id != self.SUMMONERS_RIFT:
                        vision_min = filler
                    self.imgui.add_text(f'{vision_min:^20}')

                    self.imgui.add_text(f'{cs_min:^15}')

                    self.imgui.add_text(f'{damage_min:^20}')
                # endregion Row 2: Champion, Spell, Key Rune, Items, KDA, Vision, CS, Damage

                # region Row 3: Spell, Sub Rune, Items, KDA, Vision/KP, CS, Damage
                with self.imgui.table_row():
                    with self.imgui.group(horizontal=True):
                        self.imgui.add_spacer(width=champ_size[0])

                        if not self.ui.check_image_cache('spell-' + spell_f.name):
                            spell_f_used = self.ui.load_image(
                                'spell-' + spell_f.name, self.ui.PIL, spell_f_used, size=spell_size
                            )
                        else:
                            spell_f_used = self.ui.load_image(spell_f_used, size=spell_size)
                        self.imgui.add_image(texture_tag=spell_f_used)

                        if queue == 'Arena':
                            self.imgui.add_image(
                                texture_tag='CACHED_IMAGE-filler',
                                width=sec_rune_size[0],
                                height=sec_rune_size[1],
                            )
                        elif not self.ui.check_image_cache(f'rune-{runes_taken["secondary"]["name"]}'):
                            secondary_rune_used = self.ui.load_image(
                                'rune-' + runes_taken['secondary']['name'],
                                self.ui.PIL,
                                secondary_rune_used,
                                size=sec_rune_size,
                            )
                            self.imgui.add_image(texture_tag=secondary_rune_used)
                        else:
                            secondary_rune_used = self.ui.load_image(
                                f'rune-{runes_taken["secondary"]["name"]}',
                                size=sec_rune_size,
                            )
                            self.imgui.add_image(texture_tag=secondary_rune_used)

                    # Show the last 3 items, and the trinket
                    counter = 0
                    with self.imgui.group(horizontal=True):
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
                                    self.imgui.add_image(texture_tag=image)
                                # Handle cases where there are <3 items
                                else:
                                    self.imgui.add_image(
                                        texture_tag='CACHED_IMAGE-filler',
                                        width=item_size[0],
                                        height=item_size[1],
                                    )
                            # Just iterate to the 4th item
                            else:
                                counter += 1

                    self.imgui.add_text(f'{k_d_a_display:^15}')

                    if match.map.id != self.SUMMONERS_RIFT:
                        vision = filler
                    self.imgui.add_text(f'{vision:^20}')

                    self.imgui.add_text(f'{total_cs:^15}')

                    self.imgui.add_text(f'{damage:^20}')
                # endregion Row 3: Spell, Sub Rune, Items, KDA, Vision/KP, CS, Damage

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=5)

            self.imgui.set_table_row_color(
                table=self.history,
                row=row_count,
                color=background_color,
            )
            row_count += 1

        # After all matches are shown

        # region Friends Played With
        font = self.ui.font['20 regular']
        if len(self.players_played_with.friends) > 0:
            with self.imgui.table_row(before='match_history-friends-ref'):
                with self.imgui.group():
                    self.imgui.add_spacer(height=35)
                    self.imgui.add_text('Friends Played With', tag='match_history-friends-header')
                    self.imgui.add_spacer(height=5)
                    self.imgui.add_separator()
                    self.imgui.add_spacer(height=10)
            self.imgui.bind_item_font('match_history-friends-header', self.ui.font['24 bold'])

            for PlayerPlayedWith in self.players_played_with.friends:
                with self.imgui.table_row(before='match_history-friends-ref'):
                    with self.imgui.group():
                        with self.imgui.group(horizontal=True):
                            icon_name = f'summoner_icon-{PlayerPlayedWith.summoner.profile_icon.id}'

                            # TODO: Make a UI method from this
                            if not self.ui.check_image_cache(icon_name):
                                mask = Image.open('./assets/circular_mask.png').convert('L')
                                icon = ImageOps.fit(
                                    PlayerPlayedWith.summoner.profile_icon.image, mask.size, centering=(0.5, 0.5)
                                )
                                icon.putalpha(mask)
                                icon.save(f'./data/image_cache/{icon_name}.png')

                            summoner_icon_texture = self.ui.load_image(
                                icon_name,
                                size=(30, 30),
                            )

                            self.imgui.add_image(texture_tag=summoner_icon_texture)

                            self.imgui.add_button(
                                label=PlayerPlayedWith.username,
                                enabled=False,
                                tag=f'friend-{PlayerPlayedWith.clean_username}',
                            )
                        self.imgui.add_spacer(height=2)
                        self.imgui.add_text(
                            f'{PlayerPlayedWith.win_rate:>2.1f}% WR in {PlayerPlayedWith.games_played:>3} games'
                        )
                        self.imgui.add_spacer(height=15)

                with self.imgui.theme() as item_theme:
                    with self.imgui.theme_component(self.imgui.mvButton, enabled_state=False):
                        self.imgui.add_theme_color(self.imgui.mvThemeCol_Button, (255, 255, 255))
                        self.imgui.add_theme_color(self.imgui.mvThemeCol_ButtonActive, (255, 255, 255))
                        self.imgui.add_theme_color(self.imgui.mvThemeCol_ButtonHovered, (255, 255, 255))
                        self.imgui.add_theme_color(self.imgui.mvThemeCol_Text, (0, 0, 0))
                        self.imgui.add_theme_style(self.imgui.mvStyleVar_FrameRounding, 15)
                        self.imgui.add_theme_style(self.imgui.mvStyleVar_FramePadding, 7, 5)
                self.imgui.bind_item_theme(f'friend-{PlayerPlayedWith.clean_username}', item_theme)
                self.imgui.bind_item_font(f'friend-{PlayerPlayedWith.clean_username}', font)
        # endregion Friends Played With

        # region Handler and Callback for moving champ icons when the window is resized
        def resize_call(sender):
            # Get the match id
            match_id = sender.split('-')[-1]

            # Move the image
            self.imgui.set_item_pos(
                item=f'champ-icon-{match_id}',
                pos=self.imgui.get_item_pos(f'champ-icon-holder-{match_id}'),
            )

        # Add a handler for when match data is visible, so we can get the position at that time
        with self.imgui.item_handler_registry():
            for icon in champ_icons:
                self.imgui.add_item_resize_handler(callback=resize_call, tag=f'resize_handler-{icon}')
        self.imgui.bind_item_handler_registry(self.ui.screen, self.imgui.last_container())
        # endregion Handler and Callback for moving champ icons when the window is resized

    def delete_previous_screens(self, delete_history: bool = False, delete_current: bool = False):
        if self.imgui.does_item_exist('login'):
            self.imgui.delete_item('login')

        if self.imgui.does_item_exist('loading'):
            self.imgui.delete_item('loading')

        if delete_history:
            if self.imgui.does_item_exist('match_history'):
                self.imgui.delete_item('match_history')

        if delete_current:
            if self.imgui.does_item_exist(self.ui.screen):
                self.imgui.delete_item(self.ui.screen)

    def track_lanes(self, position, outcome):
        # TODO: Implement lane popularity/wr
        self.lanes_played

    def track_champions(self, champion, outcome):
        # TODO: Implement champion popularity/wr
        self.champions_played

    def __del__(self):
        self.ui.clear_screen()
