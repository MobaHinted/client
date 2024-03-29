#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import cassiopeia
import hinter


class PlayerPlayedWith:
    username: str
    clean_username: str
    owning_user: str
    player: cassiopeia.core.match.Participant
    summoner: cassiopeia.core.match.Summoner  # TODO: why is the /last/ summoner used for icon?
    ally: bool
    outcomes: list[dict]
    _win_rate_value: float
    _win_rate_calculated: bool = False

    # TODO: add docstrings for everything, implement __str__ so PlayersPlayedWith can cache more easily

    def __init__(self, player: cassiopeia.core.match.Participant, user_outcome: str, same_team_as_user: bool):
        self.summoner: cassiopeia.core.match.Summoner = player.summoner
        self.player = player

        self.clean_username = self.summoner.sanitized_name
        self.username = self.summoner.name

        # This logic works because we only care about their ally-ship with us in the most recent game, as such,
        # this requires the match history be ordered by most recent game first
        self.ally = same_team_as_user

        self.outcomes = []

        outcome = True if user_outcome == 'Victory' else False if user_outcome == 'Defeat' else None
        self.outcomes.append(
            {
                'champion': player.champion,
                'outcome': outcome,
                'friend': same_team_as_user,
            }
        )

        self.owning_user = hinter.settings.active_user

    def add(self, champion: cassiopeia.core.match.Champion, user_outcome: str, same_team_as_user: bool):
        outcome = True if user_outcome == 'Victory' else False if user_outcome == 'Defeat' else None
        self.outcomes.append(
            {
                'champion': champion,
                'outcome': outcome,
                'friend': same_team_as_user,
            }
        )

    def __calculate_win_rate(self):
        running_total = 0
        count = 0
        for game in self.outcomes:
            if game['outcome'] is None:
                continue

            running_total += 1 if game['outcome'] else 0
            count += 1

        if count == 0:
            percentage = 100.0
        else:
            percentage = running_total / count * 100
        self._win_rate_value = float(f'{percentage:.1f}')
        self._win_rate_calculated = True
        return self._win_rate_value

    @property
    def win_rate(self) -> float:
        if not self._win_rate_calculated:
            return self.__calculate_win_rate()
        else:
            return self._win_rate_value

    @property
    def games_played(self) -> int:
        return len(self.outcomes)
