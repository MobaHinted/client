from typing import Union

import cassiopeia
import hinter

# TODO: Change imports like this one to just import hinter - in this case, maybe hinter.struct
from hinter.struct.PlayerPlayedWith import PlayerPlayedWith


class PlayersPlayedWith:
    _players_played_with: dict[str, PlayerPlayedWith] = {}

    def __init__(self):
        pass

    def add(self, player: cassiopeia.core.match.Participant, user_outcome: str, same_team_as_user: bool):
        if player.summoner.sanitized_name not in self._players_played_with.keys():
            self._players_played_with[player.summoner.sanitized_name] = PlayerPlayedWith(
                player,
                user_outcome,
                same_team_as_user
            )
        else:
            self._players_played_with[player.summoner.sanitized_name].add(
                player.champion,
                user_outcome,
                same_team_as_user
            )

    def _trim_players_played_with(self, allied: Union[bool, None], minimum_games: int = 1) -> list[PlayerPlayedWith]:
        trimmed_list = []

        for player in self._players_played_with.values():
            was_allied = (player.ally == allied) if allied is not None else True
            if was_allied and len(player.outcomes) > minimum_games:
                trimmed_list.append(player)

        return trimmed_list

    def _sort_players_played_with(self, allied: Union[bool, None], minimum_games: int = 1) -> list[PlayerPlayedWith]:
        """
        This method gives a sorted list of players played with, based on whether they were allied or not (or
        indifferent to that fact).

        .. warning::
            Private

        :param allied: Pass-through for :meth:`_trim_players_played_with`
        :param minimum_games: Pass-through for :meth:`_trim_players_played_with`
        :return: Sorted list of players played with, all players, allied players, or enemy players
        """
        return sorted(
            self._trim_players_played_with(allied, minimum_games),
            key=lambda x: x.win_rate,
            reverse=True
        )

    @property
    def _sorted_players_played_with(self) -> list[PlayerPlayedWith]:
        return self._sort_players_played_with(allied=None)

    @property
    def allies(self) -> list[PlayerPlayedWith]:
        return self._sort_players_played_with(allied=True)

    @property
    def friends(self) -> list[PlayerPlayedWith]:
        return self._sort_players_played_with(allied=True, minimum_games=hinter.settings.friend_threshold)

    @property
    def enemies(self) -> list[PlayerPlayedWith]:
        return self._sort_players_played_with(allied=False)

    def __iter__(self):
        return iter(self._sorted_players_played_with)
