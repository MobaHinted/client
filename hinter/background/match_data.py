from typing import TypedDict, Required, Union

import cassiopeia

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
    teams_background_colors: Required[list[list[float]]]  # List of lists as it's split by team
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
    _match: cassiopeia.core.match.Match

    def __init__(self, game: int, user: str = None):
        self.game = None
        self._match = hinter.cassiopeia.get_match(game, hinter.settings.region)

        self._format_game()

        if user is not None:
            self._format_game_for(user)

    def _format_game(self) -> None:
        self.game = GameReturn(
            match_id=self._match_id,
            map_id=self._map_id,
        )

    def _format_game_for(self, user) -> None:
        pass

    @property
    def _match_id(self) -> int:
        return int(self._match.id)

    @property
    def _map_id(self) -> int:
        return self._match.map.id
