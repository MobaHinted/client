import hinter
import cassiopeia


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

        with hinter.imgui.theme(tag='blue_team_bans-theme'):
            with hinter.imgui.theme_component(hinter.imgui.mvImageButton, enabled_state=False):
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FrameBorderSize, 2, 2)
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FramePadding, 1, 1)
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_Border, hinter.data.constants.TEAM_BLUE_COLOR)
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_Button, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_ButtonActive, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_ButtonHovered, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_BorderShadow, (0, 0, 0, 0))
        with hinter.imgui.theme(tag='red_team_bans-theme'):
            with hinter.imgui.theme_component(hinter.imgui.mvImageButton, enabled_state=False):
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FrameBorderSize, 2, 2)
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FramePadding, 1, 1)
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_Border, hinter.data.constants.TEAM_RED_COLOR)
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_Button, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_ButtonActive, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_ButtonHovered, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_BorderShadow, (0, 0, 0, 0))

        with hinter.imgui.group(parent='match_breakdown', horizontal=True):
            for ban in self.match['teams_bans'][self.blue_team]:
                image = hinter.imgui.add_image_button(
                    ban,
                    width=hinter.data.constants.ICON_SIZE_BAN[0],
                    height=hinter.data.constants.ICON_SIZE_BAN[1],
                    enabled=False,
                )
                hinter.imgui.bind_item_theme(image, 'blue_team_bans-theme')
        with hinter.imgui.group(parent='match_breakdown', horizontal=True):
            for ban in self.match['teams_bans'][self.red_team]:
                image = hinter.imgui.add_image_button(
                    ban,
                    width=hinter.data.constants.ICON_SIZE_BAN[0],
                    height=hinter.data.constants.ICON_SIZE_BAN[1],
                    enabled=False,
                )
                hinter.imgui.bind_item_theme(image, 'red_team_bans-theme')

        with hinter.imgui.group(parent='match_breakdown', horizontal=True):
            for item in self.match['players_items'][self.red_team][4][0:4]:
                hinter.imgui.add_image(item, width=hinter.data.constants.ICON_SIZE_ITEM[0])
        with hinter.imgui.group(parent='match_breakdown', horizontal=True):
            for item in self.match['players_items'][self.red_team][4][4:8]:
                hinter.imgui.add_image(item, width=hinter.data.constants.ICON_SIZE_ITEM[0])
