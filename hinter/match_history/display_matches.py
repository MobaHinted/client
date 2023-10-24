#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

from typing import Union

import hinter

champ_icons = []
selectables = []


# noinspection DuplicatedCode
def display_match(table: str, render: bool, game: hinter.GameData, row_count: int):
    global champ_icons
    global selectables

    hinter.imgui.add_table_row(parent=table, tag=f'match-{game["match_id"]}')

    with hinter.imgui.group(horizontal=True, parent=f'match-{game["match_id"]}'):
        with hinter.imgui.table(header_row=False, no_clip=True):
            # region Columns
            hinter.imgui.add_table_column()  # Outcome, champ played, spells, runes
            hinter.imgui.add_table_column()  # Lane, items
            hinter.imgui.add_table_column()  # Game Type, kda
            hinter.imgui.add_table_column()  # Vision, kp
            hinter.imgui.add_table_column()  # CS
            hinter.imgui.add_table_column()  # Match duration info, dmg
            # endregion Columns

            # region Row 1: Outcome, Lane, Game Type, Match duration info
            with hinter.imgui.table_row():
                hinter.imgui.add_text(game['outcome'])
                hinter.imgui.bind_item_font(hinter.imgui.last_item(), hinter.UI.font['24 regular'])

                if game['map_id'] != hinter.data.constants.SUMMONERS_RIFT_MAP_ID:
                    _ = ''
                    hinter.imgui.add_text(f'{_:^15}')
                else:
                    hinter.imgui.add_text(game['role'])

                hinter.imgui.add_text(f'{game["queue"]:^12}')

                hinter.imgui.add_spacer()
                hinter.imgui.add_spacer()

                hinter.imgui.add_text(f'{game["match_duration"]:>20}')
            # endregion Row 1: Outcome, Lane, Game Type, Match duration info

            # region Row 2: Champion, Spell, Key Rune, Items, KDA, Vision, CS, Damage
            with hinter.imgui.table_row():
                with hinter.imgui.group(horizontal=True):
                    # region Champion Icon
                    champion_played = hinter.UI.load_image(
                        f'champion-{game["player"].champion.name}',
                        hinter.data.constants.IMAGE_TYPE_PIL,
                        game['player'].champion.image,
                        size=hinter.data.constants.ICON_SIZE_CHAMPION,
                    )

                    # Place a filler image for the champion icon (hack to span 2 rows)
                    hinter.imgui.add_image(
                        texture_tag=hinter.UI.filler_image,
                        width=hinter.data.constants.ICON_SIZE_CHAMPION[0],
                        height=hinter.data.constants.ICON_SIZE_RUNE[1],
                        tag=f'champ-icon-holder-{game["match_id"]}',
                    )
                    # Draw a frame
                    hinter.UI.render_frames(split=not render)

                    champ_icons.append(f'champ-icon-{game["match_id"]}')
                    # Place the champion icon over the filler image
                    hinter.imgui.add_image(
                        texture_tag=champion_played,
                        tag=f'champ-icon-{game["match_id"]}',
                        parent='match_history',
                        pos=hinter.imgui.get_item_pos(f'champ-icon-holder-{game["match_id"]}')
                    )
                    # endregion Champion Icon

                    hinter.imgui.add_image(texture_tag=game['summoner_spells'][0])

                    hinter.imgui.add_spacer()
                    hinter.imgui.add_image(texture_tag=game['key_rune'])

                # Show the first 4 items (well, the first 3 and a spacer)
                with hinter.imgui.group(horizontal=True):
                    for item_image in game['items'][0:4]:
                        hinter.imgui.add_image(
                            texture_tag=item_image,
                            width=hinter.data.constants.ICON_SIZE_ITEM[0],
                            height=hinter.data.constants.ICON_SIZE_ITEM[1],
                        )

                kda = f'{game["kda"]} KDA'
                hinter.imgui.add_text(f'{kda:^12}')

                vision = game['vision']
                if game['map_id'] != hinter.data.constants.SUMMONERS_RIFT_MAP_ID:
                    vision = ''
                hinter.imgui.add_text(f'{vision:^20}')

                hinter.imgui.add_text(f'{game["cs"]:^15}')

                damage = f'{game["damage"]} ({game["damage_of_team"]})'
                hinter.imgui.add_text(f'{damage:^20}')
            # endregion Row 2: Champion, Spell, Key Rune, Items, KDA, Vision, CS, Damage

            # region Row 3: Spell, Sub Rune, Items, KDA, Vision/KP, CS, Damage
            with hinter.imgui.table_row():
                with hinter.imgui.group(horizontal=True):
                    hinter.imgui.add_spacer(width=hinter.data.constants.ICON_SIZE_CHAMPION[0])

                    hinter.imgui.add_image(texture_tag=game['summoner_spells'][1])

                    hinter.imgui.add_spacer(width=3)
                    if game['queue'] != 'Arena':
                        hinter.imgui.add_image(texture_tag=game['secondary_rune'])
                    else:
                        hinter.imgui.add_image(texture_tag=hinter.UI.filler_image)

                # Show the last 3 items, and the trinket
                with hinter.imgui.group(horizontal=True):
                    for item_image in game['items'][4:8]:
                        hinter.imgui.add_image(
                            texture_tag=item_image,
                            width=hinter.data.constants.ICON_SIZE_ITEM[0],
                            height=hinter.data.constants.ICON_SIZE_ITEM[1],
                        )

                hinter.imgui.add_text(f'{game["k_d_a"]:^12} {game["kp"]} KP')

                vision = game['vision_per_min']
                if game['map_id'] != hinter.data.constants.SUMMONERS_RIFT_MAP_ID:
                    vision = ''
                hinter.imgui.add_text(f'{vision:^20}')

                hinter.imgui.add_text(f'{game["cs_per_min"]:^15}')

                hinter.imgui.add_text(f'{game["damage_per_min"]:^20}')
            # endregion Row 3: Spell, Sub Rune, Items, KDA, Vision/KP, CS, Damage

            with hinter.imgui.table_row():
                hinter.imgui.add_spacer(height=5)

        # Selectable to be able to click row
        if game['queue'] != 'Arena':
            hinter.imgui.add_selectable(
                span_columns=True,
                height=115,
                callback=lambda: hinter.MatchBreakdown(game["match_id"]),
                tag=f'selectable-{game["match_id"]}',
                enabled=False,
            )
            selectables.append(f'selectable-{game["match_id"]}')

    hinter.imgui.set_table_row_color(
        table=table,
        row=row_count,
        color=game['background_color'],
    )

    hinter.UI.render_frames(render)


# Handler and Callback for moving champ icons when the window is resized
def add_row_handlers(screen):
    global champ_icons
    global selectables

    for selectable in selectables:
        hinter.imgui.configure_item(selectable, enabled=True)

    # noinspection DuplicatedCode
    def resize_call(sender):
        # Get the match id
        match_id = sender.split('-')[-1]

        # Move the image
        hinter.imgui.set_item_pos(
            item=f'champ-icon-{match_id}',
            pos=hinter.imgui.get_item_pos(f'champ-icon-holder-{match_id}'),
        )

    # Add a handler for when match data is visible, so we can get the position at that time
    with hinter.imgui.item_handler_registry(tag='match_history_handlers'):
        for icon in champ_icons:
            hinter.imgui.add_item_resize_handler(callback=resize_call, tag=f'resize_handler-{icon}')
    hinter.imgui.bind_item_handler_registry(screen, hinter.imgui.last_container())


# noinspection DuplicatedCode
def show_friends_played_with(
        players_played_with: Union[hinter.PlayersPlayedWith.PlayersPlayedWith, str],
):
    font = hinter.UI.font['20 regular']

    # Delete cached friends
    for alias in hinter.imgui.get_aliases():
        if alias.startswith('friend_row-'):
            hinter.imgui.delete_item(item=alias)

    # Load cached friends
    if players_played_with == 'cached':
        players_played_with = hinter.PlayersPlayedWith.PlayersPlayedWith(load_from_cache=True)

    if len(players_played_with.friends) > 0:
        # Draw the friends played with header once
        if not hinter.imgui.does_item_exist('friends-spacer'):
            with hinter.imgui.table_row(before='match_history-friends-ref', tag='friends-spacer'):
                with hinter.imgui.group():
                    hinter.imgui.add_spacer(height=35)
                    hinter.imgui.add_text('Friends Played With', tag='match_history-friends-header')
                    hinter.imgui.add_spacer(height=5)
                    hinter.imgui.add_separator()
                    hinter.imgui.add_spacer(height=10)
            hinter.imgui.bind_item_font('match_history-friends-header', hinter.UI.font['24 bold'])

        for PlayerPlayedWith in players_played_with.friends:
            with hinter.imgui.table_row(
                    before='match_history-friends-ref',
                    tag=f'friend_row-{PlayerPlayedWith.clean_username}'
            ):
                with hinter.imgui.group():
                    with hinter.imgui.group(horizontal=True):
                        summoner_icon_texture = hinter.UI.load_and_round_image(
                            f'summoner_icon-{PlayerPlayedWith.summoner.profile_icon.id}',
                            hinter.data.constants.IMAGE_TYPE_PIL,
                            PlayerPlayedWith.summoner.profile_icon,
                            size=hinter.data.constants.ICON_SIZE_FRIEND,
                        )
                        hinter.imgui.add_image(texture_tag=summoner_icon_texture)

                        hinter.imgui.add_button(
                            label=PlayerPlayedWith.username,
                            enabled=False,
                            tag=f'friend-{PlayerPlayedWith.clean_username}',
                        )
                    hinter.imgui.add_spacer(height=2)
                    hinter.imgui.add_text(
                        f'{PlayerPlayedWith.win_rate:>2.1f}% WR in {PlayerPlayedWith.games_played:>3} games'
                    )
                    hinter.imgui.add_spacer(height=15)

            with hinter.imgui.theme() as item_theme:
                with hinter.imgui.theme_component(hinter.imgui.mvButton, enabled_state=False):
                    hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_Button, (255, 255, 255))
                    hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_ButtonActive, (255, 255, 255))
                    hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_ButtonHovered, (255, 255, 255))
                    hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_Text, (0, 0, 0))
                    hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FrameRounding, 15)
                    hinter.imgui.add_theme_style(hinter.imgui.mvStyleVar_FramePadding, 7, 5)
            hinter.imgui.bind_item_theme(f'friend-{PlayerPlayedWith.clean_username}', item_theme)
            hinter.imgui.bind_item_font(f'friend-{PlayerPlayedWith.clean_username}', font)

        players_played_with.cache()
