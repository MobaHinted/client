import hinter


class MatchBreakdown:
    def __init__(self, match_id: int):
        self.match_id = match_id
        self.match = hinter.cassiopeia.get_match(self.match_id, hinter.settings.region)

        hinter.UI.clear_screen()
        hinter.UI.new_screen('match_breakdown')
        hinter.UI.new_screen('match_breakdown', set_primary=True)

        hinter.imgui.add_text('Match Breakdown', parent='match_breakdown')
