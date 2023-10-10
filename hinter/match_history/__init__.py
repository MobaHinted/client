from typing import Union

import cassiopeia
from PIL import Image, ImageOps

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
    ui: hinter.UIFunctionality
    players_played_with: hinter.PlayersPlayedWith

    def __init__(self, ui: hinter.UIFunctionality, render: bool = True):
        # Load summoner information
        user = cassiopeia.get_summoner(name=hinter.settings.active_user, region=hinter.settings.region)

        self.ui = ui
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
            self.ui.error_screens(e)

        self.level = user.level
        self.icon = user.profile_icon

        # Show the match screen and start processing the data
        self.show_match_screen(render)

    def show_match_screen(self, render: bool = True):
        self.delete_previous_screens()
        self.ui.new_screen(tag='match_history')

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
                            hinter.imgui.bind_item_font(hinter.imgui.last_item(), self.ui.font['40 bold'])

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
                                icon_name = f'summoner_icon-{self.icon.id}'

                                # TODO: Make a UI method from this
                                if not self.ui.check_image_cache(icon_name):
                                    mask = Image.open(
                                        f'{hinter.data.constants.PATH_ASSETS}circular_mask.png'
                                    ).convert('L')
                                    icon = ImageOps.fit(self.icon.image, mask.size, centering=(0.5, 0.5))
                                    icon.putalpha(mask)
                                    icon.save(f'{hinter.data.constants.PATH_IMAGES}{icon_name}.png')

                                summoner_icon_texture = self.ui.load_image(
                                    icon_name,
                                    size=(35, 35),
                                )

                                # Show the icon
                                hinter.imgui.add_image(texture_tag=summoner_icon_texture, tag='summoner_icon')

                                # Show the rank name
                                hinter.imgui.add_text(f'Level {self.level}')
                                hinter.imgui.bind_item_font(hinter.imgui.last_item(), self.ui.font['32 bold'])

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
                                        rank_icon_texture = self.ui.load_image(
                                            'rank-' + self.rank.tier.name,
                                            hinter.data.constants.IMAGE_TYPE_FILE,
                                            hinter.data.constants.PATH_RANKED_EMBLEMS + 'emblem-'
                                            + self.rank.tier.name + '.png',
                                            (477, 214, 810, 472),
                                            (86, 60),
                                        )
                                        hinter.imgui.add_image(texture_tag=rank_icon_texture)

                                        # Show the rank name
                                        rank_name = self.rank.division.value
                                        hinter.imgui.add_text(rank_name)
                                        hinter.imgui.bind_item_font(hinter.imgui.last_item(), self.ui.font['56 bold'])

                                    hinter.imgui.add_spacer()

                with hinter.imgui.table_row(tag='match_history-friends-ref'):
                    hinter.imgui.add_spacer()

        MatchDisplay.show_friends_played_with(self.ui, 'cached')
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
                hinter.imgui.add_table_column(tag='match-history-delete-5')
                hinter.imgui.add_table_column()  # Actual destination for matches
                hinter.imgui.add_table_column(tag='match-history-delete-6')

                with hinter.imgui.table_row(tag='match-history-delete-1'):
                    hinter.imgui.add_spacer(tag='match-history-delete-2')
                    hinter.imgui.add_text(
                        'Loading Match History. Waiting for Rito...\n\nIf this is your first time seeing this:' +
                        '\nIt can take a couple minutes',
                        tag='match-history-delete-3',
                    )
                    hinter.imgui.add_spacer(tag='match-history-delete-4')
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

        # Display screen
        hinter.imgui.set_viewport_min_width(hinter.settings.default_width)
        hinter.imgui.set_viewport_width(hinter.settings.width)
        hinter.imgui.set_viewport_min_height(hinter.settings.default_height)
        hinter.imgui.set_viewport_height(hinter.settings.height)
        self.ui.new_screen(tag='match_history', set_primary=True)

        self.ui.render_frames(60, split=not render)

    def delete_previous_screens(self, delete_history: bool = False, delete_current: bool = False):
        if hinter.imgui.does_item_exist('login'):
            hinter.imgui.delete_item('login')

        if hinter.imgui.does_item_exist('loading'):
            hinter.imgui.delete_item('loading')

        if delete_history:
            if hinter.imgui.does_item_exist('match_history'):
                hinter.imgui.delete_item('match_history')

        if delete_current:
            if hinter.imgui.does_item_exist(self.ui.screen):
                hinter.imgui.delete_item(self.ui.screen)
