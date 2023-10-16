#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import hinter


class MatchBreakdown:
    def __init__(self, match_id: int, focus_user: str = ''):
        self.match_id = match_id

        if focus_user == '':
            focus_user = hinter.settings.active_user

        data = hinter.MatchData(self.match_id, focus_user)

        self.match = data.match
        self.blue_team = data.blue_team
        self.red_team = data.red_team

        del data

        hinter.UI.clear_screen()
        hinter.UI.new_screen('match_breakdown')
        hinter.UI.new_screen('match_breakdown', set_primary=True)

        # TODO: Why does this work, but not clicking a user from the menu?

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

        with hinter.imgui.table(
                tag=f'match_breakdown-layout-{self.match_id}',
                parent='match_breakdown',
                header_row=False,
                no_clip=True
        ):
            hinter.imgui.add_table_column(init_width_or_weight=0.2)
            hinter.imgui.add_table_column()

        with hinter.imgui.table_row(parent=f'match_breakdown-layout-{self.match_id}'):
            hinter.imgui.add_text('Accolades')

            with hinter.imgui.table(tag=f'match_breakdown-{self.match_id}', header_row=False, no_clip=True):
                hinter.imgui.add_table_column()
                hinter.imgui.add_table_column(init_width_or_weight=0.1)
                hinter.imgui.add_table_column()

                with hinter.imgui.table_row():
                    with hinter.imgui.group(horizontal=True):
                        for ban in self.match['teams_bans'][self.blue_team]:
                            image = hinter.imgui.add_image_button(
                                ban,
                                width=hinter.data.constants.ICON_SIZE_BAN[0],
                                height=hinter.data.constants.ICON_SIZE_BAN[1],
                                enabled=False,
                            )
                            hinter.imgui.bind_item_theme(image, 'blue_team_bans-theme')
                        hinter.imgui.add_text(f'{"Blue Team":<{hinter.UI.find_text_for_size(480)}}')
                        hinter.imgui.add_text(f'{self.match["teams_outcomes"][self.blue_team]:>7}')

                    hinter.imgui.add_spacer()

                    with hinter.imgui.group(horizontal=True):
                        hinter.imgui.add_text(f'{self.match["teams_outcomes"][self.red_team]:<7}')
                        hinter.imgui.add_text(f'{"Red Team":>{hinter.UI.find_text_for_size(480)}}')
                        for ban in self.match['teams_bans'][self.red_team]:
                            image = hinter.imgui.add_image_button(
                                ban,
                                width=hinter.data.constants.ICON_SIZE_BAN[0],
                                height=hinter.data.constants.ICON_SIZE_BAN[1],
                                enabled=False,
                            )
                            hinter.imgui.bind_item_theme(image, 'red_team_bans-theme')

                with hinter.imgui.table_row():
                    with hinter.imgui.table(
                        tag=f'match_breakdown-{self.match_id}-blue_team',
                        header_row=False,
                        no_clip=True
                    ):
                        hinter.imgui.add_table_column()

                    hinter.imgui.add_spacer()

                    with hinter.imgui.table(
                        tag=f'match_breakdown-{self.match_id}-red_team',
                        header_row=False,
                        no_clip=True
                    ):
                        hinter.imgui.add_table_column()

        with hinter.imgui.group(parent='match_breakdown', horizontal=True):
            for item in self.match['players_items'][self.red_team][4][0:4]:
                hinter.imgui.add_image(item, width=hinter.data.constants.ICON_SIZE_ITEM[0])
        with hinter.imgui.group(parent='match_breakdown', horizontal=True):
            for item in self.match['players_items'][self.red_team][4][4:8]:
                hinter.imgui.add_image(item, width=hinter.data.constants.ICON_SIZE_ITEM[0])

    def _draw_bans(self):
        pass

    def _draw_team(self, team):
        for player_position, _ in enumerate(self.match['players_roles'][team]):
            self._draw_player(team, player_position)

    def _draw_player(self, team, player):
        player = self.match['players'][team][player]
        pass

    def blue_team(self):
        self._draw_team(self.blue_team)

    def red_team(self):
        self._draw_team(self.red_team)
