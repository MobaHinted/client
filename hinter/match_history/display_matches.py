from typing import Union

from PIL import Image, ImageOps

import hinter

champ_icons = []


# noinspection DuplicatedCode
def display_match(table, ui, render, game, row_count):
    global champ_icons
    champ_size = (64, 64)
    rune_size = (30, 30)
    sec_rune_size = (22, 22)
    spell_size = (30, 30)
    item_size = (30, 30)
    counter = 0

    hinter.imgui.add_table_row(parent=table, tag=f'match-{game["match_id"]}')

    with hinter.imgui.table(parent=f'match-{game["match_id"]}', header_row=False, no_clip=True):
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
            hinter.imgui.bind_item_font(hinter.imgui.last_item(), ui.font['24 regular'])

            hinter.imgui.add_text(game['role'])

            hinter.imgui.add_text(f'{game["queue"]:^15}')

            hinter.imgui.add_spacer()
            hinter.imgui.add_spacer()

            hinter.imgui.add_text(f'{game["duration"]:>20}')
        # endregion Row 1: Outcome, Lane, Game Type, Match duration info

        # region Row 2: Champion, Spell, Key Rune, Items, KDA, Vision, CS, Damage
        with hinter.imgui.table_row(height=rune_size[1]):
            with hinter.imgui.group(horizontal=True):
                if not ui.check_image_cache('champion-' + game['player'].champion.name):
                    champion_played = game['player'].champion.image.image
                else:
                    champion_played = 'champion-' + game['player'].champion.name

                if not ui.check_image_cache('champion-' + game['player'].champion.name):
                    champion_played = ui.load_image(
                        'champion-' + game['player'].champion.name, hinter.data.constants.IMAGE_TYPE_PIL,
                        champion_played, size=champ_size
                    )
                else:
                    champion_played = ui.load_image(champion_played, size=champ_size)

                # Place a filler image for the champion icon (hack to span 2 rows)
                hinter.imgui.add_image(
                    texture_tag=ui.filler_image,
                    width=champ_size[0],
                    height=rune_size[1],
                    tag=f'champ-icon-holder-{game["match_id"]}',
                )
                # Draw a frame
                ui.render_frames(render)

                champ_icons.append(f'champ-icon-{game["match_id"]}')
                # Place the champion icon over the filler image
                hinter.imgui.add_image(
                    texture_tag=champion_played,
                    tag=f'champ-icon-{game["match_id"]}',
                    parent='match_history',
                    pos=hinter.imgui.get_item_pos(f'champ-icon-holder-{game["match_id"]}')
                )

                if not ui.check_image_cache('spell-' + game['spell_d']['name']):
                    game['spell_d']['image'] = ui.load_image(
                        'spell-' + game['spell_d']['name'],
                        hinter.data.constants.IMAGE_TYPE_PIL,
                        game['spell_d']['image'],
                        size=spell_size
                    )
                else:
                    game['spell_d']['image'] = ui.load_image(game['spell_d']['image'], size=spell_size)
                hinter.imgui.add_image(texture_tag=game['spell_d']['image'])

                if game['queue'] == 'Arena':
                    hinter.imgui.add_image(
                        texture_tag=ui.filler_image,
                        width=rune_size[0],
                        height=rune_size[1],
                    )
                elif not ui.check_image_cache(f'rune-{game["key_rune_used"]["name"]}'):
                    key_rune_used = ui.load_image(
                        'rune-' + game['key_rune_used']['name'],
                        hinter.data.constants.IMAGE_TYPE_PIL,
                        game['key_rune_used']['image'], size=rune_size
                    )
                    hinter.imgui.add_image(texture_tag=key_rune_used)
                else:
                    key_rune_used = ui.load_image(game['key_rune_used']['image'], size=rune_size)
                    hinter.imgui.add_image(texture_tag=key_rune_used)

            # Show the first 3 items
            with hinter.imgui.group(horizontal=True):
                for item in game['items']:
                    if counter < 3:
                        # Load the image if it is not a placeholder
                        if item['item'] != 'filler':
                            if not ui.check_image_cache(f'item-{item["item"]}'):
                                image = ui.load_image(
                                    'item-' + str(item['item']), hinter.data.constants.IMAGE_TYPE_PIL,
                                    item['image'], size=item_size
                                )
                            else:
                                image = ui.load_image(f'item-{item["item"]}', size=item_size)
                            hinter.imgui.add_image(texture_tag=image)
                        # Handle cases where there are <3 items
                        else:
                            hinter.imgui.add_image(
                                texture_tag=ui.filler_image,
                                width=item_size[0],
                                height=item_size[1],
                            )
                    else:
                        continue
                    counter += 1
                # Filler '4th item' in this row to show above trinket
                hinter.imgui.add_image(
                    texture_tag=ui.filler_image,
                    width=item_size[0],
                    height=item_size[1],
                )

            hinter.imgui.add_text(f'{game["kda_display"]:^15}')

            if game['map_id'] != hinter.data.constants.SUMMONERS_RIFT_MAP_ID:
                game['vision_min'] = ''
            hinter.imgui.add_text(f'{game["vision_min"]:^20}')

            hinter.imgui.add_text(f'{game["cs_min"]:^15}')

            hinter.imgui.add_text(f'{game["damage_min"]:^20}')
        # endregion Row 2: Champion, Spell, Key Rune, Items, KDA, Vision, CS, Damage

        # region Row 3: Spell, Sub Rune, Items, KDA, Vision/KP, CS, Damage
        with hinter.imgui.table_row():
            with hinter.imgui.group(horizontal=True):
                hinter.imgui.add_spacer(width=champ_size[0])

                if not ui.check_image_cache('spell-' + game['spell_f']['name']):
                    spell_f_used = ui.load_image(
                        'spell-' + game['spell_f']['name'],
                        hinter.data.constants.IMAGE_TYPE_PIL,
                        game['spell_f']['image'],
                        size=spell_size
                    )
                else:
                    spell_f_used = ui.load_image(game['spell_f']['image'], size=spell_size)
                hinter.imgui.add_image(texture_tag=spell_f_used)

                if game['queue'] == 'Arena':
                    hinter.imgui.add_image(
                        texture_tag=ui.filler_image,
                        width=sec_rune_size[0],
                        height=sec_rune_size[1],
                    )
                elif not ui.check_image_cache(f'rune-{game["secondary_rune_used"]["name"]}'):
                    secondary_rune_used = ui.load_image(
                        'rune-' + game['secondary_rune_used']['name'],
                        hinter.data.constants.IMAGE_TYPE_PIL,
                        game['secondary_rune_used']['image'],
                        size=sec_rune_size,
                    )
                    hinter.imgui.add_image(texture_tag=secondary_rune_used)
                else:
                    secondary_rune_used = ui.load_image(
                        f'rune-{game["secondary_rune_used"]["name"]}',
                        size=sec_rune_size,
                    )
                    hinter.imgui.add_image(texture_tag=secondary_rune_used)

            # Show the last 3 items, and the trinket
            counter = 0
            with hinter.imgui.group(horizontal=True):
                for item in game['items']:
                    # Skip the first 3 items
                    if counter >= 3:
                        # Load the image if it is not a placeholder
                        if item['item'] != 'filler':
                            if not ui.check_image_cache(f'item-{item["item"]}'):
                                image = ui.load_image(
                                    'item-' + str(item['item']), hinter.data.constants.IMAGE_TYPE_PIL,
                                    item['image'], size=item_size
                                )
                            else:
                                image = ui.load_image(f'item-{item["item"]}', size=item_size)
                            hinter.imgui.add_image(texture_tag=image)
                        # Handle cases where there are <3 items
                        else:
                            hinter.imgui.add_image(
                                texture_tag=ui.filler_image,
                                width=item_size[0],
                                height=item_size[1],
                            )
                    # Just iterate to the 4th item
                    else:
                        counter += 1

            hinter.imgui.add_text(f'{game["k_d_a_display"]:^15}')

            if game['map_id'] != hinter.data.constants.SUMMONERS_RIFT_MAP_ID:
                game['vision'] = ''
            hinter.imgui.add_text(f'{game["vision"]:^20}')

            hinter.imgui.add_text(f'{game["total_cs"]:^15}')

            hinter.imgui.add_text(f'{game["damage"]:^20}')
        # endregion Row 3: Spell, Sub Rune, Items, KDA, Vision/KP, CS, Damage

        with hinter.imgui.table_row():
            hinter.imgui.add_spacer(height=5)

    hinter.imgui.set_table_row_color(
        table=table,
        row=row_count,
        color=game['background_color'],
    )

    ui.render_frames(render)


# Handler and Callback for moving champ icons when the window is resized
def add_row_handlers(screen):
    global champ_icons

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
    with hinter.imgui.item_handler_registry():
        for icon in champ_icons:
            hinter.imgui.add_item_resize_handler(callback=resize_call, tag=f'resize_handler-{icon}')
    hinter.imgui.bind_item_handler_registry(screen, hinter.imgui.last_container())


# noinspection DuplicatedCode
def show_friends_played_with(
        ui: hinter.UIFunctionality,
        players_played_with: Union[hinter.PlayersPlayedWith.PlayersPlayedWith, str],
):
    font = ui.font['20 regular']

    # Load cached friends
    if players_played_with == 'cached':
        players_played_with = hinter.PlayersPlayedWith.PlayersPlayedWith(load_from_cache=True)

    if len(players_played_with.friends) > 0:
        # Delete cached friends
        if hinter.imgui.does_item_exist('friends-spacer'):
            hinter.imgui.delete_item(item='friends-spacer')
            for PlayerPlayedWith in players_played_with.friends:
                hinter.imgui.delete_item(item=f'friend_row-{PlayerPlayedWith.clean_username}')

        with hinter.imgui.table_row(before='match_history-friends-ref', tag='friends-spacer'):
            with hinter.imgui.group():
                hinter.imgui.add_spacer(height=35)
                hinter.imgui.add_text('Friends Played With', tag='match_history-friends-header')
                hinter.imgui.add_spacer(height=5)
                hinter.imgui.add_separator()
                hinter.imgui.add_spacer(height=10)
        hinter.imgui.bind_item_font('match_history-friends-header', ui.font['24 bold'])

        for PlayerPlayedWith in players_played_with.friends:
            with hinter.imgui.table_row(
                    before='match_history-friends-ref',
                    tag=f'friend_row-{PlayerPlayedWith.clean_username}'
            ):
                with hinter.imgui.group():
                    with hinter.imgui.group(horizontal=True):
                        icon_name = f'summoner_icon-{PlayerPlayedWith.summoner.profile_icon.id}'

                        # TODO: Make a UI method from this
                        if not ui.check_image_cache(icon_name):
                            mask = Image.open(f'{hinter.data.constants.PATH_ASSETS}circular_mask.png').convert('L')
                            icon = ImageOps.fit(
                                PlayerPlayedWith.summoner.profile_icon.image, mask.size, centering=(0.5, 0.5)
                            )
                            icon.putalpha(mask)
                            icon.save(f'{hinter.data.constants.PATH_IMAGES}{icon_name}.png')

                        summoner_icon_texture = ui.load_image(
                            icon_name,
                            size=(30, 30),
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
