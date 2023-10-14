#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import cassiopeia

from hinter.match_history import MatchHistory
# noinspection PyPep8Naming
import hinter.match_history.display_matches as MatchDisplay
import hinter


# noinspection DuplicatedCode
class HistoryData(MatchHistory):
    champ_icons: list
    player: cassiopeia.core.match.Participant
    players_played_with: hinter.PlayersPlayedWith.PlayersPlayedWith

    def __init__(self, render: bool):
        super().__init__(render)
        self.players_played_with = hinter.PlayersPlayedWith.PlayersPlayedWith()
        self.load_matches()

    def load_matches(self, render: bool = True):
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
            match = hinter.MatchData(match.id, hinter.settings.active_user).match
            MatchDisplay.display_match(self.history, render, match, row_count)
            row_count += 1

        MatchDisplay.add_row_handlers('match_history')
        MatchDisplay.show_friends_played_with(self.players_played_with)
