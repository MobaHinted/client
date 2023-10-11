import datetime
from typing import Union

import cassiopeia
import pytz
import timeago
import timeago.locales.en  # Required for building to executable
from PIL import Image

from hinter.match_history import MatchHistory
# noinspection PyPep8Naming
import hinter.match_history.display_matches as MatchDisplay
import hinter


# noinspection DuplicatedCode
class HistoryData(MatchHistory):
    game: dict
    champ_icons: list
    player: cassiopeia.core.match.Participant
    players_played_with: hinter.PlayersPlayedWith.PlayersPlayedWith
    ui: hinter.UIFunctionality

    def __init__(self, ui: hinter.UIFunctionality, render: bool):
        super().__init__(ui, render)
        self.ui = ui
        self.players_played_with = hinter.PlayersPlayedWith.PlayersPlayedWith()
        self.load_matches()

    def load_matches(self, render: bool = True):
        self.game = {}
        self.champ_icons = []

        # Have filler if the user has not been in any games
        if not self.games:
            with hinter.imgui.table_row(parent=self.history):
                hinter.imgui.add_spacer()
                hinter.imgui.add_text('There are no games for this user, yet!')
                hinter.imgui.add_spacer()
            return

        # region Remove loading info
        hinter.imgui.delete_item(item='match-history-delete-1')
        hinter.imgui.delete_item(item='match-history-delete-2')
        hinter.imgui.delete_item(item='match-history-delete-3')
        hinter.imgui.delete_item(item='match-history-delete-4')
        hinter.imgui.delete_item(item='match-history-delete-5')
        hinter.imgui.delete_item(item='match-history-delete-6')
        # endregion Remove loading info

        row_count = 0
        # Loop through the games
        # noinspection PyTypeChecker
        for _, match in enumerate(self.games[0:hinter.settings.match_history_count]):
            match: cassiopeia.Match
            self._assemble_basic_match_info(match)
            self._calculate_match_data(match)
            self._get_items()
            self._get_runes()
            MatchDisplay.display_match(self.history, self.ui, render, self.game, row_count)
            row_count += 1

        MatchDisplay.add_row_handlers('match_history')
        MatchDisplay.show_friends_played_with(self.ui, self.players_played_with)

    # TODO: Move the actual data getting and formatting to background.match_data

    def _assemble_basic_match_info(self, match: cassiopeia.Match):
        self.game = {
            'match_id': match.id,
            'map_id': match.map.id,
        }

        # region Setup multiple variables
        team_kills: int = 0
        team_damage: int = 0
        # endregion Setup multiple variables

        # region Determine type of game
        # Handle old matches that can't be loaded
        # noinspection PyBroadException
        try:
            queue = match.queue.name
        except Exception:
            return

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

        self.game['queue'] = queue
        # endregion Determine type of game

        # region Determine stats of user whose match history this is
        for participant in match.participants:
            if participant.summoner.name == self.username:
                self.game['team'] = participant.side.name
                self.game['player'] = participant
        # endregion Determine stats of user whose match history this is

        # region Resolve ending condition of game
        if match.is_remake:
            win = 'Remake'
            self.game['background_color'] = hinter.data.constants.MATCH_COLOR_REMAKE
        else:
            if self.game['player'].stats.win:
                win = 'Victory'
                self.game['background_color'] = hinter.data.constants.MATCH_COLOR_WIN
            else:
                win = 'Defeat'
                self.game['background_color'] = hinter.data.constants.MATCH_COLOR_LOSS

        self.game['outcome'] = win
        # endregion Resolve ending condition of game

        # TODO: track champions played here

        # region Track players played with
        for participant in match.participants:
            if participant.summoner.name != self.username:
                self.players_played_with.add(
                    participant,
                    self.game['outcome'],
                    participant.side.name == self.game['team']
                )
        # endregion Track players played with

        # region Determine player's team's kill count
        for participant in match.participants:
            if participant.side.name == self.game['team']:
                team_kills += participant.stats.kills
                team_damage += participant.stats.total_damage_dealt_to_champions
        self.game['team_kills'] = team_kills
        self.game['team_damage'] = team_damage
        # endregion Determine player's team's kill count

    def _calculate_match_data(self, match: cassiopeia.Match):
        player: cassiopeia.core.match.Participant = self.game['player']

        # region Match Timing
        # Calculate match length in minutes
        match_length_parts = str(match.duration).split(':')
        match_minutes = int(match_length_parts[0] * 60)
        match_minutes += int(match_length_parts[1])
        match_minutes += (int(match_length_parts[2]) / 60)
        match_minutes = round(match_minutes, 2)

        # Calculate when the match happened
        now = datetime.datetime.now()
        now = pytz.utc.localize(now)
        match_time = datetime.datetime.fromisoformat(
            str(match.creation)
        )

        # Format match timing and how long ago it was
        # duration = str(match.duration) + ' long - '  # HH:MM:SS display
        duration = f'{match_minutes:>2.0f}min - '
        duration += timeago.format(match_time, now)
        self.game['duration'] = duration.replace('utes', '')
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

        self.game['spell_d'] = {'name': spell_d.name, 'image': spell_d_used}
        self.game['spell_f'] = {'name': spell_f.name, 'image': spell_f_used}
        # endregion Summoner Spells

        # region Role
        # Only check any lane/role data if this is summoner's rift
        position: cassiopeia.data.Position = cassiopeia.data.Position.none
        if match.map.id == hinter.data.constants.SUMMONERS_RIFT_MAP_ID:
            # Determine role of player
            if hasattr(player.stats, 'role'):
                role = str(player.stats.role)
            else:
                role = str(player.role)
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
        if match.map.id != hinter.data.constants.SUMMONERS_RIFT_MAP_ID:
            played_position = ''
        # Change 'utility' to 'support'
        elif position == cassiopeia.data.Position.utility:
            played_position = 'Support'
        else:
            played_position = position.name.capitalize()

        self.game['role'] = played_position

        # TODO: track role played here
        # endregion Role

        # region KDA and KP
        # Calculate KDA
        kills_assists = player.stats.kills + player.stats.assists
        kda = kills_assists
        if player.stats.deaths != 0:  # Avoid dividing my zero
            kda /= player.stats.deaths
        kda = round(kda, 2)  # Trim off excess decimal places

        self.game['kda_display'] = f'{kda:.1f} KDA'
        self.game['k_d_a_display'] = (str(player.stats.kills) + ' / ' + str(player.stats.deaths) +
                                      ' / ' + str(player.stats.assists))

        # Calculate KP (avoiding division by zero)
        kill_participation = kills_assists / (self.game['team_kills'] + 0.00000001) * 100
        kill_participation = int(round(kill_participation, 0))
        # endregion KDA and KP

        # region Damage
        damage = player.stats.total_damage_dealt_to_champions
        damage_of_team = int(round(damage / (self.game['team_damage'] + 0.00000001) * 100, 0))
        damage_min = int(round(damage / match_minutes, 0))
        self.game['damage_min'] = f'{damage_min:,} DMG/Min'
        if self.game['queue'] != 'Arena':
            damage = f'{damage:,} DMG - {damage_of_team}%'
        else:
            damage = f'{damage:,} DMG'
        self.game['damage'] = damage
        # endregion Damage

        # region Vision
        # Calculate Vision/Min
        vision_min = round(player.stats.vision_score / match_minutes, 2)
        self.game['vision_min'] = str(vision_min) + ' Vis/Min'

        # Show vision score and kill participation
        self.game['vision'] = (str(player.stats.vision_score) + ' Vis - ' +
                               str(kill_participation) + '% KP')
        # endregion Vision

        # region Creep Score (CS) stats
        cs_gotten = player.stats.total_minions_killed
        cs_gotten += player.stats.neutral_minions_killed
        cs_min = round(cs_gotten / match_minutes, 1)
        self.game['cs_min'] = str(cs_min) + ' CS/Min'
        self.game['total_cs'] = f'{cs_gotten:,} CS'
        # endregion Creep Score (CS) stats

    def _get_items(self):
        player_items = self.game['player'].stats.items
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
        for item in player_items:
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

        self.game['items'] = items

    def _get_runes(self):
        player: cassiopeia.core.match.Participant = self.game['player']

        # region Runes Taken
        # Structure what runes the player took
        if self.game['queue'] != 'Arena':
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
        # Load the keystone rune
        self.game['key_rune_used'] = {
            'name': runes_taken['key']['name'],
            'image': runes_taken['key']['image']
        }

        # Load the secondary rune tree
        self.game['secondary_rune_used'] = {
            'name': runes_taken['secondary']['name'],
            'image': runes_taken['secondary']['image']
        }
