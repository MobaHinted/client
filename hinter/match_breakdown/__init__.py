import hinter
import roleidentification.utilities as casiopeia_role_identification


class MatchBreakdown:
    def __init__(self, match_id: int):
        self.match_id = match_id

        data = hinter.MatchData(self.match_id)

        self.match = data.match
        self.blue_team = data.blue_team
        self.red_team = data.red_team

        del data

        hinter.UI.clear_screen()
        hinter.UI.new_screen('match_breakdown')
        hinter.UI.new_screen('match_breakdown', set_primary=True)

        # TODO: Why does this work, but not clicking a user from the menu?

        hinter.imgui.add_text(f'Match Breakdown: {self.match_id}', parent='match_breakdown')
        hinter.imgui.add_separator(parent='match_breakdown')
        hinter.imgui.add_text(f'Map: {self.match["map_id"]}', parent='match_breakdown')
