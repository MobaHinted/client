from datetime import datetime
from typing import TypedDict, Required, Union

import cassiopeia
import pytz
import timeago

import hinter


# Does not support Arena
class GameReturn(TypedDict, total=False):
    match_id: Required[int]
    map_id: Required[int]
    queue: Required[str]
    match_duration: Required[str]
    # region For individual match views
    players: Required[list[list[cassiopeia.core.match.Participant]]]
    teams_kills: Required[list[int]]
    teams_damage: Required[list[int]]
    teams_outcomes: Required[list[str]]
    teams_background_colors: Required[list[list[int]]]  # List of lists as it's split by team
    players_summoner_spells: Required[list[list[str]]]
    players_roles: Required[list[list[str]]]
    players_kdas: Required[list[list[str]]]
    players_k_d_as: Required[list[list[str]]]
    players_damage: Required[list[list[int]]]
    players_damage_of_team: Required[list[list[int]]]
    players_damage_per_min: Required[list[list[int]]]
    players_vision: Required[list[list[int]]]
    players_vision_per_min: Required[list[list[float]]]
    players_kp: Required[list[list[float]]]
    players_cs: Required[list[list[int]]]
    players_cs_per_min: Required[list[list[float]]]
    players_items: Required[list[list[list[dict]]]]
    players_key_runes: Required[list[list[dict]]]
    players_secondary_runes: Required[list[list[dict]]]
    players_runes: Required[list[list[list[dict]]]]
    # endregion For individual match views
    # region For Match History
    player: cassiopeia.core.match.Participant
    team: str
    team_kills: int
    team_damage: int
    outcome: str
    background_color: list[float]
    summoner_spells: list[str]
    role: str
    kda: str
    k_d_a: str
    damage: int
    damage_of_team: int
    damage_per_min: int
    vision: int
    vision_per_min: float
    kp: float
    cs: int
    cs_per_min: float
    items: list[dict]
    key_rune: dict
    secondary_rune: dict
    runes: list[dict]
    # endregion For Match History


class MatchData:
    game: Union[GameReturn, None]
    blue_team: int  # The keys to use when splitting the match data by team
    red_team: int
    _match: cassiopeia.core.match.Match
    _teams_damage_values: Union[list[int], None]
    _teams_background_colors_values: Union[list[list[int]], None]

    def __init__(self, game: int, user: str = None):
        self.game = None
        self._teams_damage_values = None
        self._teams_background_colors_values = None
        self._match = hinter.cassiopeia.get_match(game, hinter.settings.region)

        # Just done here programmatically, so it's easier to adjust for if ever needed,
        # or possibly to aid in supporting other game modes in the future
        teams = [cassiopeia.data.Side.blue, cassiopeia.data.Side.red]
        self.blue_team = teams.index(cassiopeia.data.Side.blue)
        self.red_team = teams.index(cassiopeia.data.Side.red)

        self._format_game()

        if user is not None:
            self._format_game_for(user)

    def _format_game(self) -> None:
        self.game = GameReturn(
            match_id=self._match_id,
            map_id=self._map_id,
            queue=self._queue,
            match_duration=self._match_duration,
        )

    def _format_game_for(self, user) -> None:
        pass

    def _assemble_into_teams(self, blue_team_data: list, red_team_data: list) -> list[list]:
        teamed_data = []
        # Again done here like this to adjust or support other game modes
        teamed_data[self.blue_team] = blue_team_data
        teamed_data[self.red_team] = red_team_data

        return teamed_data

    @property
    def _match_id(self) -> int:
        return int(self._match.id)

    @property
    def _map_id(self) -> int:
        return self._match.map.id

    @property
    def _queue(self) -> str:
        # noinspection PyBroadException
        try:
            queue = self._match.queue.name
        except Exception:
            return ''

        # Shorter names for the queue static data
        ranked = cassiopeia.data.Queue.ranked_solo_fives
        flex = cassiopeia.data.Queue.ranked_flex_fives
        clash = cassiopeia.data.Queue.clash
        blind = cassiopeia.data.Queue.blind_fives
        draft = cassiopeia.data.Queue.normal_draft_fives
        aram = cassiopeia.data.Queue.aram
        arena = cassiopeia.data.Queue.rings_of_wrath

        if self._match.queue == ranked or self._match.queue == ranked.name:
            queue = 'Ranked Solo'
        elif self._match.queue == flex or self._match.queue == flex.name:
            queue = 'Ranked Flex'
        elif self._match.queue == clash or self._match.queue == clash.name:
            queue = 'Clash'
        elif self._match.queue == blind or self._match.queue == blind.name:
            queue = 'Normal Blind'
        elif self._match.queue == draft or self._match.queue == draft.name:
            queue = 'Normal Draft'
        elif self._match.queue == aram or self._match.queue == aram.name:
            queue = 'ARAM'
        elif self._match.queue == arena or self._match.queue == arena.name:
            queue = 'Arena'
        else:
            queue = queue.replace('_', ' ').title()

        return queue

    @property
    def _match_duration(self) -> str:
        match_length_parts = str(self._match.duration).split(':')
        match_minutes = int(match_length_parts[0] * 60)
        match_minutes += int(match_length_parts[1])
        match_minutes += int(match_length_parts[2]) / 60
        self._match_minutes = round(match_minutes, 2)

        # Calculate when the match happened
        now = datetime.now()
        now = pytz.utc.localize(now)
        match_time = datetime.fromisoformat(
            str(self._match.creation)
        )

        # Format match timing and how long ago it was
        # duration = str(self._match.duration) + ' long - '  # HH:MM:SS display
        duration = f'{self._match_minutes:>2.0f}min - '
        duration += timeago.format(match_time, now)
        return duration.replace('utes', '')

    @property
    def _players(self) -> list[list[cassiopeia.core.match.Participant]]:
        blue_team = []
        red_team = []

        for participant in self._match.participants:
            if participant.side == cassiopeia.data.Side.blue:
                blue_team.append(participant)
            else:
                red_team.append(participant)

        return self._assemble_into_teams(blue_team, red_team)

    @property
    def _teams_kills(self) -> list[int]:
        teams_kills = [0, 0]
        teams_damage = [0, 0]

        for team, players in enumerate(self._players):
            for player in players:
                teams_kills[team] += player.stats.kills
                teams_damage[team] += player.stats.total_damage_dealt_to_champions

        self._teams_damage_values = teams_damage

        return teams_kills

    @property
    def _teams_damage(self) -> list[int]:
        if self._teams_damage_values is None:
            # noinspection PyStatementEffect
            self._teams_kills

        return self._teams_damage_values

    @property
    def _teams_outcomes(self) -> list[str]:
        # Short-circuit for remakes
        if self._match.is_remake:
            self._teams_background_colors_values = [
                hinter.data.constants.MATCH_COLOR_REMAKE,
                hinter.data.constants.MATCH_COLOR_REMAKE
            ]
            return ['Remake', 'Remake']

        teams_outcomes = []
        background_colors = []

        for team, player in enumerate(self._players):
            if player[0].stats.win:
                teams_outcomes[team] = 'Victory'
                background_colors[team] = hinter.data.constants.MATCH_COLOR_WIN
            else:
                teams_outcomes[team] = 'Defeat'
                background_colors[team] = hinter.data.constants.MATCH_COLOR_LOSS

        return teams_outcomes

    @property
    def _teams_background_colors(self) -> list[list[int]]:
        if self._teams_background_colors_values is None:
            # noinspection PyStatementEffect
            self._teams_outcomes

        return self._teams_background_colors_values

    @property
    def _players_summoner_spells(self) -> list[list[str]]:
        pass



