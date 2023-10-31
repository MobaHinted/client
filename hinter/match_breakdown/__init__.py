#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #
import threading

import cassiopeia.core.match
import hinter


class MatchBreakdown:
    def __init__(self, match_id: int, focus_user: str = ''):
        self.match_id = match_id
        self.champ_icons = []

        if focus_user == '':
            focus_user = hinter.settings.active_user

        data = hinter.MatchData(self.match_id, focus_user)

        self.match = data.match
        self.blue_team = data.blue_team
        self.red_team = data.red_team

        self.forwards = self.blue_team
        self.backwards = self.red_team

        del data

        # TODO: Why does this work, but not clicking a user from the menu / clicking Match History?
        hinter.UI.clear_screen()
        hinter.UI.new_screen('match_breakdown')
        hinter.UI.new_screen('match_breakdown', set_primary=True)

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
        with hinter.imgui.theme(tag='blue_team_damage-theme'):
            with hinter.imgui.theme_component(hinter.imgui.mvProgressBar):
                hinter.imgui.add_theme_color(
                    hinter.imgui.mvThemeCol_PlotHistogram,
                    hinter.data.constants.TEAM_BLUE_COLOR
                )
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FrameRounding, 15)
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FramePadding, 7, 5)
        with hinter.imgui.theme(tag='red_team_damage-theme'):
            with hinter.imgui.theme_component(hinter.imgui.mvProgressBar):
                hinter.imgui.add_theme_color(
                    hinter.imgui.mvThemeCol_PlotHistogram,
                    hinter.data.constants.TEAM_RED_COLOR
                )
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FrameRounding, 15)
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FramePadding, 7, 5)
        with hinter.imgui.theme(tag='no_padding_theme'):
            with hinter.imgui.theme_component(hinter.imgui.mvAll):
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_ItemSpacing, 0, 0)
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FramePadding, 0, 0)
        with hinter.imgui.theme(tag='vertical_padding_theme'):
            with hinter.imgui.theme_component(hinter.imgui.mvAll):
                hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FramePadding, 0, 5)

        with hinter.imgui.table(
                tag=f'match_breakdown-layout-{self.match_id}',
                parent='match_breakdown',
                header_row=False,
                no_clip=True
        ):
            hinter.imgui.add_table_column(init_width_or_weight=0.15)
            hinter.imgui.add_table_column()

        hinter.imgui.bind_item_theme(f'match_breakdown-layout-{self.match_id}', 'no_padding_theme')

        with (hinter.imgui.table_row(parent=f'match_breakdown-layout-{self.match_id}')):
            hinter.imgui.add_text('Accolades')

            with hinter.imgui.table(tag=f'match_breakdown-{self.match_id}', header_row=False):
                hinter.imgui.add_table_column()
                hinter.imgui.add_table_column(init_width_or_weight=0.1)
                hinter.imgui.add_table_column()

                with hinter.imgui.table_row():
                    with hinter.imgui.table(header_row=False):
                        # region Spacing header text
                        hinter.imgui.add_table_column(init_width_or_weight=0.05)
                        hinter.imgui.add_table_column(init_width_or_weight=0.67)
                        hinter.imgui.add_table_column()
                        hinter.imgui.add_table_column(init_width_or_weight=0.36)
                        hinter.imgui.add_table_column()
                        hinter.imgui.add_table_column(init_width_or_weight=0.42)
                        hinter.imgui.add_table_column(init_width_or_weight=0.05)
                        # endregion Spacing header text

                        with hinter.imgui.table_row():
                            hinter.imgui.add_spacer()

                            with hinter.imgui.group(horizontal=True):
                                for ban in self.match['teams_bans'][self.blue_team]:
                                    image = hinter.imgui.add_image_button(
                                        ban,
                                        width=hinter.data.constants.ICON_SIZE_BAN[0],
                                        height=hinter.data.constants.ICON_SIZE_BAN[1],
                                        enabled=False,
                                    )
                                    hinter.imgui.bind_item_theme(image, 'blue_team_bans-theme')
                                    hinter.imgui.add_spacer(width=4)

                            hinter.imgui.add_spacer()

                            hinter.imgui.add_text('Blue Team')
                            hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                            hinter.imgui.add_spacer()

                            outcome = hinter.imgui.add_text(self.match["teams_outcomes"][self.blue_team])
                            hinter.imgui.bind_item_font(outcome, hinter.UI.font['24 regular'])
                            hinter.imgui.bind_item_theme(outcome, 'vertical_padding_theme')

                            hinter.imgui.add_spacer()

                    hinter.imgui.add_spacer()

                    with hinter.imgui.table(header_row=False):
                        # region Spacing header text
                        hinter.imgui.add_table_column(init_width_or_weight=0.05)
                        hinter.imgui.add_table_column(init_width_or_weight=0.42)
                        hinter.imgui.add_table_column()
                        hinter.imgui.add_table_column(init_width_or_weight=0.36)
                        hinter.imgui.add_table_column()
                        hinter.imgui.add_table_column(init_width_or_weight=0.67)
                        hinter.imgui.add_table_column(init_width_or_weight=0.05)
                        # endregion Spacing header text

                        with hinter.imgui.table_row():
                            hinter.imgui.add_spacer()

                            outcome = hinter.imgui.add_text(self.match["teams_outcomes"][self.red_team])
                            hinter.imgui.bind_item_font(outcome, hinter.UI.font['24 regular'])
                            hinter.imgui.bind_item_theme(outcome, 'vertical_padding_theme')

                            hinter.imgui.add_spacer()

                            hinter.imgui.add_text('Red Team')
                            hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                            hinter.imgui.add_spacer()

                            with hinter.imgui.group(horizontal=True):
                                for ban in self.match['teams_bans'][self.red_team]:
                                    hinter.imgui.add_spacer(width=4)
                                    image = hinter.imgui.add_image_button(
                                        ban,
                                        width=hinter.data.constants.ICON_SIZE_BAN[0],
                                        height=hinter.data.constants.ICON_SIZE_BAN[1],
                                        enabled=False,
                                    )
                                    hinter.imgui.bind_item_theme(image, 'red_team_bans-theme')

                            hinter.imgui.add_spacer()

                with hinter.imgui.table_row():
                    with hinter.imgui.table(
                        tag=f'match_breakdown-{self.match_id}-blue_team',
                        header_row=False,
                        no_clip=True
                    ):
                        hinter.imgui.add_table_column()

                        with hinter.imgui.table_row(tag='blue_team_loading'):
                            with hinter.imgui.table(header_row=False):
                                hinter.imgui.add_table_column()
                                hinter.imgui.add_table_column()
                                hinter.imgui.add_table_column()

                                with hinter.imgui.table_row():
                                    hinter.imgui.add_spacer()
                                    with hinter.imgui.group(horizontal=True):
                                        hinter.imgui.add_spacer(width=120,height=1)
                                        hinter.imgui.add_loading_indicator()

                        with hinter.imgui.table_row(tag='blue_team-ref'):
                            hinter.imgui.add_spacer()

                    hinter.imgui.add_spacer()

                    with hinter.imgui.table(
                        tag=f'match_breakdown-{self.match_id}-red_team',
                        header_row=False,
                        no_clip=True
                    ):
                        hinter.imgui.add_table_column()

                        with hinter.imgui.table_row(tag='red_team_loading'):
                            with hinter.imgui.table(header_row=False):
                                hinter.imgui.add_table_column()
                                hinter.imgui.add_table_column()
                                hinter.imgui.add_table_column()

                                with hinter.imgui.table_row():
                                    hinter.imgui.add_spacer()
                                    with hinter.imgui.group(horizontal=True):
                                        hinter.imgui.add_spacer(width=60,height=1)
                                        hinter.imgui.add_loading_indicator()

                        with hinter.imgui.table_row(tag='red_team-ref'):
                            hinter.imgui.add_spacer()

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(width=20,height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_text('Stats...')

        thread = threading.Thread(target=self.draw_teams)
        thread.start()

    def _draw_bans(self):
        pass

    def _draw_team(self, team: int):
        for player_position, _ in enumerate(self.match['players_roles'][team]):
            if team == self.blue_team:
                before = 'blue_team-ref'
                tag = f'blue_team-player_{player_position}'
            else:
                before = 'red_team-ref'
                tag = f'red_team-player_{player_position}'

            with hinter.imgui.table_row(before=before, show=False, tag=tag):
                self._draw_player(team, player_position, team)

    def _draw_player(self, team: int, player: int, direction: int):
        # noinspection PyTypeChecker
        participant: cassiopeia.core.match.Participant = self.match['players'][team][player]

        def champ_icon():
            # noinspection PyTypeChecker,PyUnresolvedReferences
            champion = self.match['players'][team][player].champion

            champion_played = hinter.UI.load_image(
                f'champion-{champion.name}',
                hinter.data.constants.IMAGE_TYPE_PIL,
                champion.image,
                size=hinter.data.constants.ICON_SIZE_CHAMPION,
            )

            # Place a filler image for the champion icon (hack to span 2 rows)
            hinter.imgui.add_image(
                texture_tag=hinter.UI.filler_image,
                width=hinter.data.constants.ICON_SIZE_CHAMPION[0],
                height=hinter.data.constants.ICON_SIZE_RUNE[1],
                tag=f'champ_icon_holder-{team}_{player}',
            )

            self.champ_icons.append(f'{team}_{player}')
            # Place the champion icon over the filler image
            hinter.imgui.add_image(
                texture_tag=champion_played,
                tag=f'champ_icon-{team}_{player}',
                parent='match_breakdown',
                pos=(-1000, -1000)
            )

        with hinter.imgui.table(header_row=False):
            # region Columns
            hinter.imgui.add_table_column()
            hinter.imgui.add_table_column()
            hinter.imgui.add_table_column()
            hinter.imgui.add_table_column()
            hinter.imgui.add_table_column()
            # endregion Columns

            with hinter.imgui.table_row():
                # TODO: MVP / ACE / etc could go here
                hinter.imgui.add_spacer(height=20)

            cs = self.match["players_cs"][team][player] + ' (' + \
                self.match["players_cs_per_min"][team][player].replace(' CS', '') + ')'
            kp = self.match["players_kps"][team][player] + ' KP'

            with hinter.imgui.table_row():
                if direction == self.forwards:
                    with hinter.imgui.group(horizontal=True):
                        champ_icon()
                        hinter.imgui.add_spacer(width=5)
                        hinter.imgui.add_image(
                            self.match['players_key_runes'][team][player]
                        )
                        hinter.imgui.add_spacer(width=3)
                        hinter.imgui.add_image(
                            self.match['players_summoner_spells'][team][player][0],
                        )

                    hinter.imgui.add_text(f'{participant.summoner.name:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    with hinter.imgui.group(horizontal=True):
                        for item in self.match['players_items'][team][player][0:4]:
                            hinter.imgui.add_image(item, width=hinter.data.constants.ICON_SIZE_ITEM[0])
                            hinter.imgui.add_spacer(width=4)

                    hinter.imgui.add_text(f'{cs:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    hinter.imgui.add_text(f'{kp:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')
                else:
                    hinter.imgui.add_text(f'{kp:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    hinter.imgui.add_text(f'{cs:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    with hinter.imgui.group(horizontal=True):
                        items = self.match['players_items'][team][player][0:4]
                        items.reverse()
                        for item in items:
                            hinter.imgui.add_spacer(width=4)
                            hinter.imgui.add_image(item, width=hinter.data.constants.ICON_SIZE_ITEM[0])

                    hinter.imgui.add_text(f'{participant.summoner.name:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    with hinter.imgui.group(horizontal=True):
                        hinter.imgui.add_image(
                            self.match['players_summoner_spells'][team][player][0],
                        )
                        hinter.imgui.add_spacer(width=6)
                        hinter.imgui.add_image(
                            self.match['players_key_runes'][team][player]
                        )
                        hinter.imgui.add_spacer(width=5)
                        champ_icon()

            damage_percent = float(
                self.match["players_damage_of_team"][team][player][0:-1]
            ) / 100
            damage_text = self.match["players_damage"][team][player] + ' ' + \
                self.match["players_damage_of_team"][team][player]

            vision = self.match['players_vision_per_min'][team][player].replace('Vis', 'Vision')

            with hinter.imgui.table_row():
                if direction == self.forwards:
                    with hinter.imgui.group(horizontal=True):
                        hinter.imgui.add_spacer(width=hinter.data.constants.ICON_SIZE_CHAMPION[0])

                        hinter.imgui.add_spacer(width=8)

                        hinter.imgui.add_image(
                            self.match['players_secondary_rune_trees'][team][player]
                        )

                        hinter.imgui.add_spacer(width=8)

                        hinter.imgui.add_image(
                            self.match['players_summoner_spells'][team][player][1],
                        )

                    hinter.imgui.add_text(f'{self.match["players_k_d_as"][team][player]:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    with hinter.imgui.group(horizontal=True):
                        for item in self.match['players_items'][team][player][4:8]:
                            hinter.imgui.add_image(item, width=hinter.data.constants.ICON_SIZE_ITEM[0])
                            hinter.imgui.add_spacer(width=4)

                    hinter.imgui.add_text(f'{vision:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    progress = hinter.imgui.add_progress_bar(
                        width=-1,
                        default_value=damage_percent,
                        overlay=f'{damage_text:^16}'
                    )
                    hinter.imgui.bind_item_theme(progress, 'blue_team_damage-theme')
                else:
                    progress = hinter.imgui.add_progress_bar(
                        width=-1,
                        default_value=damage_percent,
                        overlay=f'{damage_text:^16}'
                    )
                    hinter.imgui.bind_item_theme(progress, 'red_team_damage-theme')

                    hinter.imgui.add_text(f'{vision:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    with hinter.imgui.group(horizontal=True):
                        items = self.match['players_items'][team][player][4:8]
                        items.reverse()
                        for item in items:
                            hinter.imgui.add_spacer(width=4)
                            hinter.imgui.add_image(item, width=hinter.data.constants.ICON_SIZE_ITEM[0])

                    hinter.imgui.add_text(f'{self.match["players_k_d_as"][team][player]:^16}')
                    hinter.imgui.bind_item_theme(hinter.imgui.last_item(), 'vertical_padding_theme')

                    with hinter.imgui.group(horizontal=True):
                        hinter.imgui.add_image(
                            self.match['players_summoner_spells'][team][player][1],
                        )
                        hinter.imgui.add_spacer(width=11)
                        hinter.imgui.add_image(
                            self.match['players_secondary_rune_trees'][team][player]
                        )

    def _add_row_handlers(self):
        # noinspection DuplicatedCode
        def resize_call(sender):
            # Get the match id
            team_player = sender.split('-')[-1]

            # Move the image
            hinter.imgui.set_item_pos(
                item=f'champ_icon-{team_player}',
                pos=hinter.imgui.get_item_pos(f'champ_icon_holder-{team_player}'),
            )

        # Handling resizing
        with hinter.imgui.item_handler_registry(tag='match_breakdown_handlers'):
            for icon in self.champ_icons:
                hinter.imgui.add_item_resize_handler(callback=resize_call, tag=f'resize_handler-{icon}')
        hinter.imgui.bind_item_handler_registry('match_breakdown', hinter.imgui.last_container())

        # Handling initial positioning of champ icons
        hinter.UI.render_frames(split=True)
        for icon in self.champ_icons:
            resize_call(f'-{icon}')

    def draw_blue_team(self):
        self._draw_team(self.blue_team)

    def draw_red_team(self):
        self._draw_team(self.red_team)

    def draw_teams(self):
        self.draw_blue_team()
        self.draw_red_team()

        # region Show players
        hinter.imgui.delete_item('blue_team_loading')
        hinter.imgui.delete_item('blue_team-ref')
        hinter.imgui.delete_item('red_team_loading')
        hinter.imgui.delete_item('red_team-ref')

        hinter.imgui.show_item('blue_team-player_0')
        hinter.imgui.show_item('blue_team-player_1')
        hinter.imgui.show_item('blue_team-player_2')
        hinter.imgui.show_item('blue_team-player_3')
        hinter.imgui.show_item('blue_team-player_4')
        hinter.imgui.show_item('red_team-player_0')
        hinter.imgui.show_item('red_team-player_1')
        hinter.imgui.show_item('red_team-player_2')
        hinter.imgui.show_item('red_team-player_3')
        hinter.imgui.show_item('red_team-player_4')
        # endregion Show players

        self._add_row_handlers()
