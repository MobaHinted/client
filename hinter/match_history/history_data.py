#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import threading
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

    def __init__(self):
        super().__init__()

        thread = threading.Thread(target=self.load_matches)
        thread.start()

    def load_matches(self):
        self.champ_icons = []

        # Have filler if the user has not been in any games
        if not self.games:
            with hinter.imgui.table_row(parent=self.history):
                hinter.imgui.add_spacer()
                hinter.imgui.add_text('There are no games for this user, yet!')
                hinter.imgui.add_spacer()
            return

        # Loop through the games
        # noinspection PyTypeChecker
        for count, match in enumerate(self.games):
            # region Track players played with
            # Find the user's team
            team = 'blue'
            for participant in match.participants:
                if participant.summoner.name == self.username:
                    team = participant.side.name
            # Track each participant
            for participant in match.participants:
                if participant.summoner.name != self.username:
                    self.players_played_with.add(
                        participant,
                        'Remake' if match.is_remake else 'Victory' if participant.stats.win else 'Defeat',
                        participant.side.name == team
                    )
            # endregion Track players played with

            match = hinter.MatchData(match.id, hinter.settings.active_user).match
            MatchDisplay.display_match(self.history, match)

            hinter.imgui.configure_item(
                'match-history-progress-bar',
                default_value=count / len(self.games),
                overlay=f'Loading {count}/{len(self.games)}...',
            )

        # noinspection PyTypeChecker
        for _, match in enumerate(self.games):
            hinter.imgui.configure_item(f'match-{match.id}', show=True)

        MatchDisplay.show_friends_played_with(self.players_played_with)

        # region Remove loading info
        hinter.imgui.delete_item(item='match-history-delete-1')
        hinter.imgui.delete_item(item='match-history-delete-2')
        hinter.imgui.delete_item(item='match-history-delete-3')
        hinter.imgui.delete_item(item='match-history-delete-4')
        hinter.imgui.delete_item(item='match-history-delete-5')
        # endregion Remove loading info

        MatchDisplay.color_rows(self.history)
        MatchDisplay.add_row_handlers('match_history')
        hinter.UI.render_frames(split=True)
