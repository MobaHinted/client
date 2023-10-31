#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

from typing import Union

import cassiopeia

import hinter
import hinter.match_history.display_matches as MatchDisplay

__all__ = [
    'MatchHistory',
]


# noinspection DuplicatedCode
class MatchHistory:
    games: cassiopeia.MatchHistory
    rank: Union[cassiopeia.Rank, None]
    level = 0
    icon = 0
    username = ""
    table: str
    table_row: str
    left_bar: str
    history: str
    right_bar: str
    players_played_with: hinter.PlayersPlayedWith

    def __init__(self, render: bool = True):
        # Load summoner information
        user = cassiopeia.get_summoner(name=hinter.settings.active_user, region=hinter.settings.region)

        self.players_played_with = hinter.PlayersPlayedWith.PlayersPlayedWith()

        self.username = user.name

        # Try to load rank
        try:
            self.games = user.match_history
            # TODO: fix this in cassiopeia to get fewer calls on initial load
            # self.games = user.match_history(continent=user.region.continent, puuid=user.puuid, count=100)

            if cassiopeia.Queue.ranked_solo_fives in user.ranks:
                self.rank = user.ranks[cassiopeia.Queue.ranked_solo_fives]
            elif cassiopeia.Queue.ranked_flex_fives in user.ranks:
                self.rank = user.ranks[cassiopeia.Queue.ranked_flex_fives]
            else:
                self.rank = None

        # Error out if that code doesn't work, which indicates an API issue
        except Exception as e:
            hinter.UI.error_screens(e)

        self.level = user.level
        self.icon = user.profile_icon

        # Show the match screen and start processing the data
        self.show_match_screen()

    def show_match_screen(self):
        hinter.UI.new_screen(tag='match_history')

        # Set up the table
        self.table = hinter.imgui.add_table(
            tag='match_history_table',
            header_row=False,
            parent='match_history',
        )
        self.table_row = hinter.imgui.add_table_row(
            parent=self.table,
            tag='match_history_table-row',
        )

        # region Left Bar
        # Set up the left-bar
        self.left_bar = hinter.imgui.add_table_column(
            parent=self.table,
            tag='match_history_table-left',
            init_width_or_weight=0.2,
        )
        with (hinter.imgui.table_cell(parent=self.table_row)):
            with hinter.imgui.table(header_row=False, tag='match_history-friends-parent'):
                hinter.imgui.add_table_column()

                # User name, centered
                with hinter.imgui.table_row():
                    with hinter.imgui.table(header_row=False):
                        # Adjust widths to center username
                        #  at 40pt it can fit 17 characters, and max character length for names is 16
                        portion = 1.0 / 16
                        name_portion = portion * len(self.username)
                        spacer_portion = (1.0 - name_portion) / 2

                        hinter.imgui.add_table_column(init_width_or_weight=spacer_portion)
                        hinter.imgui.add_table_column(init_width_or_weight=name_portion)
                        hinter.imgui.add_table_column(init_width_or_weight=spacer_portion)

                        # Center the username
                        with hinter.imgui.table_row():
                            hinter.imgui.add_spacer()

                            hinter.imgui.add_text(self.username)
                            hinter.imgui.bind_item_font(hinter.imgui.last_item(), hinter.UI.font['40 bold'])

                            hinter.imgui.add_spacer()

                # Icon and level
                with hinter.imgui.table_row():
                    with hinter.imgui.table(header_row=False):
                        hinter.imgui.add_table_column(init_width_or_weight=0.2)
                        hinter.imgui.add_table_column(init_width_or_weight=0.6)
                        hinter.imgui.add_table_column(init_width_or_weight=0.2)

                        with hinter.imgui.table_row():
                            hinter.imgui.add_spacer()

                            with hinter.imgui.group(horizontal=True):
                                summoner_icon_texture = hinter.UI.load_and_round_image(
                                    f'summoner_icon-{self.icon.id}',
                                    hinter.data.constants.IMAGE_TYPE_PIL,
                                    self.icon,
                                    size=hinter.data.constants.ICON_SIZE_SUMMONER,
                                )
                                hinter.imgui.add_image(texture_tag=summoner_icon_texture, tag='summoner_icon')

                                # Show the rank name
                                hinter.imgui.add_text(f'Level {self.level}')
                                hinter.imgui.bind_item_font(hinter.imgui.last_item(), hinter.UI.font['32 bold'])

                            hinter.imgui.add_spacer()

                # Rank
                # TODO: Master+ has no division, display LP/position?
                if self.rank is not None and hinter.settings.show_my_rank:
                    with hinter.imgui.table_row():
                        with hinter.imgui.group():
                            hinter.imgui.add_spacer(height=20)
                            with hinter.imgui.table(header_row=False):
                                hinter.imgui.add_table_column(init_width_or_weight=0.275)
                                hinter.imgui.add_table_column(init_width_or_weight=0.45)
                                hinter.imgui.add_table_column(init_width_or_weight=0.275)

                                with hinter.imgui.table_row():
                                    hinter.imgui.add_spacer()

                                    with hinter.imgui.group(horizontal=True):
                                        # Show the icon
                                        rank_icon_texture = hinter.UI.load_image(
                                            'rank-' + self.rank.tier.name,
                                            hinter.data.constants.IMAGE_TYPE_FILE,
                                            hinter.data.constants.PATH_RANKED_EMBLEMS +
                                            'Rank=' + self.rank.tier.name.title() + '.png',
                                            size=hinter.data.constants.ICON_SIZE_RANK,
                                        )
                                        hinter.imgui.add_image(texture_tag=rank_icon_texture)

                                        # Show the rank name
                                        rank_name = self.rank.division.value
                                        hinter.imgui.add_text(rank_name)
                                        hinter.imgui.bind_item_font(hinter.imgui.last_item(), hinter.UI.font['56 bold'])

                                    hinter.imgui.add_spacer()

                with hinter.imgui.table_row(tag='match_history-friends-ref'):
                    hinter.imgui.add_spacer()

        MatchDisplay.show_friends_played_with('cached')
        # endregion Left Bar

        # region  Center (Match History container)
        # Set up the center column, just a container for match history
        hinter.imgui.add_table_column(
            parent=self.table,
            init_width_or_weight=0.60,
        )
        # Add a table that matches can be added to as rows, everything else is just a placeholder until the matches load
        with hinter.imgui.table_cell(parent=self.table_row):
            with hinter.imgui.table(tag='match_history_table-history-container',
                                    header_row=False, pad_outerX=True) as self.history:
                hinter.imgui.add_table_column(tag='match-history-delete-2')
                hinter.imgui.add_table_column()  # Actual destination for matches
                hinter.imgui.add_table_column(tag='match-history-delete-3')

                with hinter.imgui.table_row(tag='match-history-delete-1'):
                    hinter.imgui.add_spacer()
                    # TODO: Add back the loading indicator, once load_matches is threaded
                    hinter.imgui.add_text(
                        'Loading Match History. Waiting for Rito...\n\nIf this is your first time seeing this:' +
                        '\nIt can take a couple minutes',
                    )
                    hinter.imgui.add_spacer()

                with hinter.imgui.table_row(tag='match-history-delete-4'):
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row(tag='match-history-delete-5'):
                    hinter.imgui.add_spacer()
                    with hinter.imgui.table(header_row=False):
                        hinter.imgui.add_table_column()
                        hinter.imgui.add_table_column()
                        hinter.imgui.add_table_column()

                        with hinter.imgui.table_row():
                            hinter.imgui.add_spacer()
                            hinter.imgui.add_loading_indicator()

        with hinter.imgui.theme() as item_theme:
            with hinter.imgui.theme_component(hinter.imgui.mvTable):
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_HeaderHovered, (255, 255, 255, 50))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_HeaderActive, (255, 255, 255, 50))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_Header, (0, 0, 0, 0))
        hinter.imgui.bind_item_theme('match_history_table-history-container', item_theme)
        # endregion Center (Match History container)

        # region Right Bar
        # Set up the right-bar
        self.right_bar = hinter.imgui.add_table_column(
            parent=self.table,
            tag='match_history_table-right',
            init_width_or_weight=0.2,
        )
        with hinter.imgui.table_cell(parent=self.table_row):
            with hinter.imgui.table(header_row=False):
                hinter.imgui.add_table_column()

                with hinter.imgui.table_row():
                    hinter.imgui.add_text('role distribution, champ wr here')
        # endregion Right Bar

        hinter.UI.render_frames(split=True)

        # Display screen
        hinter.imgui.set_viewport_min_width(hinter.settings.default_width)
        hinter.imgui.set_viewport_width(hinter.settings.width)
        hinter.imgui.set_viewport_min_height(hinter.settings.default_height)
        hinter.imgui.set_viewport_height(hinter.settings.height)
        hinter.imgui.set_viewport_resizable(True)
        hinter.imgui.hide_item('loading')
        hinter.UI.new_screen(tag='match_history', set_primary=True)

