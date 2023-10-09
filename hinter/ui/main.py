import os
import webbrowser
from typing import Union

import PIL.Image as Image
import numpy as np
import requests
import cassiopeia

import hinter
# TODO: Change imports like this one to just import hinter
import hinter.background.dataloader


class UI:
    screen: str = 'login'
    font: dict = {}
    user_available: bool = False
    data_loader: hinter.background.dataloader.DataLoader
    filler_image: str
    move_on_callback: callable
    render: bool
    data_loader: hinter.background.dataloader.DataLoader
    imgui = hinter.imgui  # TODO: Remove this, import hinter.user and match history to __init__ and include that in main

    def __init__(self, move_on_callback):
        self.move_on_callback = move_on_callback
        hinter.imgui.create_context()
        self.imgui_init()

        # Set up Fira Code for use
        with hinter.imgui.font_registry():
            sizes = [16, 20, 24, 32, 40, 48, 56]
            for size in sizes:
                self.font[f'{size} regular'] = hinter.imgui.add_font(
                    f'{hinter.data.constants.PATH_ASSETS}fcr.ttf',
                    size * hinter.data.constants.UI_FONT_SCALE
                )
                self.font[f'{size} medium'] = hinter.imgui.add_font(
                    f'{hinter.data.constants.PATH_ASSETS}fcm.ttf',
                    size * hinter.data.constants.UI_FONT_SCALE
                )
                self.font[f'{size} bold'] = hinter.imgui.add_font(
                    f'{hinter.data.constants.PATH_ASSETS}fcb.ttf',
                    size * hinter.data.constants.UI_FONT_SCALE
                )
        hinter.imgui.set_global_font_scale(1 / hinter.data.constants.UI_FONT_SCALE)
        hinter.imgui.bind_font(self.font['16 medium'])

        hinter.imgui.setup_dearpygui()

        hinter.imgui.add_texture_registry(tag='images')

        hinter.imgui.create_viewport(
            # decorated=False, # Would have to add manual resizing, maximizing, etc
            title='MobaHinted',
            min_width=350,
            width=350,
            min_height=600,
            height=600,
            small_icon=f'{hinter.data.constants.PATH_ASSETS}logo.ico',
            large_icon=f'{hinter.data.constants.PATH_ASSETS}logo.ico',
            x_pos=hinter.settings.x,
            y_pos=hinter.settings.y,
        )
        hinter.imgui.set_exit_callback(self.exit_callback)

        self.filler_image = self.load_image(
            'filler',
            hinter.data.constants.IMAGE_TYPE_FILE,
            f'{hinter.data.constants.PATH_ASSETS}filler.png',
            size=(1, 1)
        )

        # region Login flow
        # TODO: Move this to a private method
        def login_submit():
            username = hinter.imgui.get_value('add-username')
            region = hinter.imgui.get_value('add-region')

            hinter.settings.write_setting('region', region)
            added = hinter.users.add_user(ui=self, username=username)

            if added:
                self.user_available = True
                hinter.settings.write_setting('active_user', username)
                self.data_loader = hinter.background.dataloader.DataLoader()
                self.render = False
                move_on_callback(ui=self, render=self.render)
                hinter.imgui.render_dearpygui_frame()

        if hinter.settings.active_user == '':
            with hinter.imgui.window(tag=self.screen):
                with hinter.imgui.table(header_row=False):
                    hinter.imgui.add_table_column(init_width_or_weight=0.15)
                    hinter.imgui.add_table_column(init_width_or_weight=0.7)
                    hinter.imgui.add_table_column(init_width_or_weight=0.15)

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer()
                        hinter.imgui.add_spacer(height=150)
                        hinter.imgui.add_spacer()

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer()
                        hinter.imgui.add_text('Add your League Account')
                        hinter.imgui.add_spacer()

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer(height=10)

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer()
                        hinter.imgui.add_input_text(
                            tag='add-username',
                            hint='League Name',
                            width=-1,
                            on_enter=True,
                            callback=login_submit,
                        )

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer()
                        with hinter.imgui.group(horizontal=True):
                            hinter.imgui.add_text('Region: ')
                            hinter.imgui.add_combo(
                                tag='add-region',
                                items=[e.value for e in cassiopeia.data.Region],
                                default_value=hinter.settings.region,
                                width=-1,
                                callback=login_submit,
                            )

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer(height=10)

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer()
                        hinter.imgui.add_button(
                            tag='add-button',
                            label='Add >',
                            width=-1,
                            callback=login_submit,
                        )

            hinter.imgui.set_primary_window(window=self.screen, value=True)
            hinter.imgui.show_viewport()
            hinter.imgui.set_viewport_resizable(False)
        # endregion Login flow
        else:
            self.user_available = True
            self.screen = 'loading'

            with hinter.imgui.window(tag=self.screen):
                with hinter.imgui.table(header_row=False):
                    hinter.imgui.add_table_column()
                    hinter.imgui.add_table_column()
                    hinter.imgui.add_table_column()

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer()
                        hinter.imgui.add_spacer(height=250)
                        hinter.imgui.add_spacer()

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer()
                        hinter.imgui.add_text('Loading')
                        hinter.imgui.add_spacer()

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer()
                        hinter.imgui.add_loading_indicator()
                        hinter.imgui.add_spacer()

            self.data_loader = hinter.background.dataloader.DataLoader()
            hinter.imgui.set_primary_window(window=self.screen, value=True)
            hinter.imgui.show_viewport()
            self.render_frames(120)
            self.render = True
            move_on_callback(ui=self, render=self.render)

    def show_info_popup(self, title: str, text: str, width: int = 225, height: int = 125):
        # Wait one frame to ensure that other modals are closed
        hinter.imgui.split_frame()

        # Ensure the popup can close itself
        def close_popup():
            hinter.imgui.delete_item(item='info-popup')
            hinter.imgui.delete_item(item='info-text')
            hinter.imgui.delete_item(item='info-spacer')
            hinter.imgui.delete_item(item='info-ok')

        # Show the popup
        with hinter.imgui.window(
                label=title,
                modal=True,
                tag='info-popup',
                width=width,
                height=height,
                no_resize=True,
                no_move=True,
                no_collapse=True,
                on_close=close_popup
        ):
            hinter.imgui.add_text(tag='info-text', default_value=text, wrap=width - 20)

            # Button to close the popup
            hinter.imgui.add_spacer(tag='info-spacer', height=10)
            hinter.imgui.add_button(
                tag='info-ok',
                parent='info-popup',
                label='Ok',
                callback=close_popup,
                width=width,
            )

        # Center the popup
        self.center_window('info-popup', [width, height])

    def add_menu(self):
        # Delete the old menu bar, if it exists, and add a new one
        if hinter.imgui.does_item_exist('menu'):
            hinter.imgui.delete_item(item='menu')

        with hinter.imgui.menu_bar(tag='menu', parent=self.screen):
            # region Settings Menu
            hinter.imgui.add_menu_item(
                label='Settings',
                callback=lambda: (
                    hinter.imgui.show_item(item='settings-popup'),
                    self.center_window('settings-popup'),
                ),
            )
            self.ready_settings_window()
            # endregion Settings Menu

            # region Data Menu
            with hinter.imgui.menu(label='Data', tag='menu-data'):
                hinter.imgui.add_menu_item(
                    label='Reload all data',
                    parent='menu-data',
                    callback=lambda: self.data_loader.load_all(refresh=True)
                )
            # endregion Data Menu

            # region User Menu
            with hinter.imgui.menu(label='User', tag='menu-user'):
                # Option to add a user
                hinter.imgui.add_menu_item(
                    label='Add User',
                    callback=lambda: (hinter.users.add_user(self)),
                )
                self.add_menu_separator()

                # List each user, with the option to remove that user
                users = hinter.users.list_users(self.screen)
                for user in users:
                    username = user.username

                    # Check if the user is the one currently selected
                    selected = ''
                    if hinter.settings.active_user == username:
                        selected = '<-'

                    # Add the user to the menu
                    hinter.imgui.add_menu_item(
                        tag=f'menu-user-{username}',
                        label=username,
                        # TODO: changing users here doesn't work. can't determine why
                        callback=lambda sender: (
                            hinter.users.select_user(sender.split('-')[-1]),
                            self.move_on_callback(ui=self, render=not self.render),
                            print('selecting new user:' + sender.split('-')[-1])
                        ),
                        shortcut=selected,
                    )

                # Option to remove a user
                if len(users) > 0:
                    self.add_menu_separator()
                    hinter.imgui.add_menu_item(
                        label='Remove User',
                        callback=lambda: (hinter.users.remove_user(self)),
                    )
            # endregion User Menu

            # region Help Menu
            with hinter.imgui.menu(label='Help', tag='menu-help'):
                hinter.imgui.add_menu_item(
                    label='Quick Guide',
                    callback=lambda: (),
                )

                self.add_menu_separator()

                hinter.imgui.add_menu_item(
                    label='Offer Feedback',
                    callback=lambda: (),
                )

                hinter.imgui.add_menu_item(
                    label='Report an Issue',
                    callback=lambda: (),
                )

                hinter.imgui.add_menu_item(
                    label='Suggest a feature',
                    callback=lambda: (),
                )

                self.add_menu_separator()

                hinter.imgui.add_menu_item(
                    label='Contribute Code',
                    callback=lambda: (),
                )
            # endregion About Menu

            # region About Menu
            with hinter.imgui.menu(label='About', tag='menu-about'):

                # noinspection SpellCheckingInspection
                hinter.imgui.add_menu_item(
                    label='''Made by zbee, mostly in season 13
Copyright 2020 Ethan Henderson
Available under the GPLv3 license
Open Source at github.com/zbee/mobahinted''',
                    enabled=False,
                )
            # endregion About Menu

    def ready_settings_window(self):
        settings_gear = self.load_image(
            'settings_gear',
            hinter.data.constants.IMAGE_TYPE_FILE,
            f'{hinter.data.constants.PATH_ASSETS}settings.png',
            size=(16, 16)
        )

        if hinter.imgui.does_item_exist(item='settings-popup'):
            return

        # Make sure the popup can be hidden
        def close_popup():
            hinter.imgui.hide_item(item='settings-popup')

        # Callback to save each setting, requires tag to be same as setting
        def save_setting(sender: str, data):
            hinter.settings.write_setting(sender, data)

            if '_separate' in sender:
                window = sender.split('_')[1]

                if data:
                    hinter.imgui.show_item(f'auto_close_{window}')
                else:
                    hinter.imgui.hide_item(f'auto_close_{window}')

            if 'overlay_' in sender:
                if data:
                    hinter.imgui.show_item(f'{sender}-config')
                else:
                    hinter.imgui.hide_item(f'{sender}-config')

            if 'pipeline' == sender:
                for pipeline in hinter.settings.pipelines.keys():
                    target = pipeline.replace(' ', '_').replace(',', '').lower()

                    if pipeline == data:
                        hinter.imgui.show_item(f'pipeline_description-{target}')
                    else:
                        hinter.imgui.hide_item(f'pipeline_description-{target}')
                del pipeline, target

        # Show the popup
        with hinter.imgui.window(
                label='Settings',
                modal=True,
                tag='settings-popup',
                width=600,
                height=550,
                no_move=True,
                no_collapse=True,
                on_close=close_popup,
                show=False,
        ):
            users = hinter.users.list_users()

            # TODO: Move to ui.settings, add generators for behavior section like the overlay section has
            with hinter.imgui.table(header_row=False, no_clip=True):
                hinter.imgui.add_table_column()
                hinter.imgui.add_table_column()
                hinter.imgui.add_table_column()
                hinter.imgui.add_table_column()

                # region Overlay Section
                with hinter.imgui.table_row():
                    hinter.imgui.add_text('Overlays')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                overlays = [
                    {
                        'overlay_milestones': 'Milestone Notifications',
                        'overlay_cs_tracker': 'CS Tracker and Stats Window',
                    },
                    {
                        'overlay_objectives': 'Objective Reminders',
                        'overlay_spell_tracker': 'Enemy Spell Tracker',
                    },
                    {
                        'overlay_jungle': 'Jungle Timers',
                        'overlay_aram': 'ARAM Health Timers',
                    },
                    {
                        'overlay_duos': 'Scoreboard Duos',
                        'overlay_gold_diff': 'Scoreboard Item Gold Diff',
                    },
                    {
                        'overlay_map_check': 'Map Check Reminder',
                        'overlay_back_reminder': 'Back Reminder',
                    },
                    {
                        'overlay_trinket': 'Use Trinket Reminder',
                        'overlay_counter_items': 'Counter Item Suggestions',
                    }
                ]

                for duo_of_overlays in overlays:
                    with hinter.imgui.table_row():
                        for tag, label in duo_of_overlays.items():
                            with hinter.imgui.group(horizontal=True):
                                hinter.imgui.add_checkbox(
                                    label=label,
                                    default_value=getattr(hinter.settings, tag),
                                    tag=tag,
                                    callback=save_setting
                                )
                                hinter.imgui.add_image_button(
                                    texture_tag=settings_gear,
                                    tag=f'{tag}-config',
                                    show=getattr(hinter.settings, tag),
                                )
                            hinter.imgui.add_spacer()

                    with hinter.imgui.table_row():
                        hinter.imgui.add_spacer(height=20)

                del duo_of_overlays, overlays

                with hinter.imgui.table_row():
                    hinter.imgui.add_button(label='View all Overlay positions')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)
                with hinter.imgui.table_row():
                    hinter.imgui.add_separator()
                    hinter.imgui.add_spacer(height=20)
                # endregion Overlay Section

                # region Behavior Section
                with hinter.imgui.table_row():
                    hinter.imgui.add_text('Application Behavior')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label='Launch MobaHinted on system startup',
                        default_value=hinter.settings.launch_on_startup,
                        tag='launch_on_startup',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label='Keep MobaHinted up to date automatically',
                        default_value=hinter.settings.automatic_updates,
                        tag='automatic_updates',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label='Close MobaHinted to the tray',
                        default_value=hinter.settings.close_to_tray,
                        tag='close_to_tray',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label='Bring MobaHinted to the front on window change',
                        default_value=hinter.settings.bring_to_front,
                        tag='bring_to_front',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label='Always show MobaHinted in the same place',
                        default_value=hinter.settings.save_window_position,
                        tag='save_window_position',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label='Detect new accounts automatically',
                        default_value=hinter.settings.detect_new_accounts,
                        tag='detect_new_accounts',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_slider_int(
                        label='Number of games to show in Match History',
                        min_value=20,
                        max_value=250,
                        default_value=hinter.settings.match_history_count,
                        tag='match_history_count',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_slider_int(
                        label='Number of games for someone to be considered a Friend',
                        min_value=2,
                        max_value=10,
                        default_value=hinter.settings.friend_threshold,
                        tag='friend_threshold',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label="Show my rank to me",
                        default_value=hinter.settings.show_my_rank,
                        tag='show_my_rank',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label="Show teammate ranks",
                        default_value=hinter.settings.show_ally_rank,
                        tag='show_ally_rank',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label="Show enemy ranks",
                        default_value=hinter.settings.show_enemy_rank,
                        tag='show_enemy_rank',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label="Show game average ranks",
                        default_value=hinter.settings.show_game_ranks,
                        tag='show_game_ranks',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label="Show the current-play-session window",
                        default_value=hinter.settings.show_current_session,
                        tag='show_current_session',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label="Show pre-game/lobby info as a separate window",
                        default_value=hinter.settings.show_pregame_separate,
                        tag='show_pregame_separate',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row(show=hinter.settings.auto_close_pregame):
                    hinter.imgui.add_checkbox(
                        label="Automatically close the Show pre-game/lobby info window",
                        default_value=hinter.settings.auto_close_pregame,
                        indent=25,
                        tag='auto_close_pregame',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label="Show pre-game build suggestions as a separate window",
                        default_value=hinter.settings.show_builds_separate,
                        tag='show_builds_separate',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row(show=hinter.settings.auto_close_pregame):
                    hinter.imgui.add_checkbox(
                        label="Automatically close the pre-game build suggestions window",
                        default_value=hinter.settings.auto_close_builds,
                        indent=25,
                        tag='auto_close_builds',
                        callback=save_setting,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(
                        label="Show post-game as a separate window",
                        default_value=hinter.settings.show_postgame_separate,
                        tag='show_postgame_separate',
                        callback=save_setting,
                    )

                # Only suitable as a development tool
                # with hinter.imgui.table_row():
                #     hinter.imgui.add_spacer(height=20)

                # with hinter.imgui.table_row():
                #     hinter.imgui.add_button(
                #         label='Customize Theme',
                #         callback=lambda: (hinter.imgui.show_style_editor()),
                #     )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)
                with hinter.imgui.table_row():
                    hinter.imgui.add_separator()
                    hinter.imgui.add_spacer(height=20)
                # endregion Behavior Section

                # region Accounts Section
                with hinter.imgui.table_row():
                    hinter.imgui.add_text('Accounts')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_text('Current Account:')
                    hinter.imgui.add_combo(
                        items=[e.username for e in users],
                        default_value=hinter.settings.active_user,
                        width=-1
                    )
                    hinter.imgui.add_text('Current Region:')
                    hinter.imgui.add_combo(
                        items=[e.value for e in cassiopeia.data.Region],
                        default_value=hinter.settings.region,
                        width=60
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_text('Add an Account:')
                    hinter.imgui.add_input_text(hint='League Name', width=-1)
                    hinter.imgui.add_text('On Region:')
                    with hinter.imgui.group(horizontal=True):
                        hinter.imgui.add_combo(
                            items=[e.value for e in cassiopeia.data.Region],
                            default_value=hinter.settings.region,
                            width=60
                        )
                        hinter.imgui.add_button(label='Add >', width=-1)

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)
                with hinter.imgui.table_row():
                    hinter.imgui.add_separator()
                    hinter.imgui.add_spacer(height=20)
                # endregion Accounts Section

                # region Privacy Section
                with hinter.imgui.table_row():
                    hinter.imgui.add_text('Privacy')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_text('Current Data Pipeline:')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=10)

                with hinter.imgui.table_row():
                    with hinter.imgui.group(horizontal=True):
                        hinter.imgui.add_combo(
                            items=list(hinter.settings.pipelines.keys()),
                            default_value=hinter.settings.pipeline,
                            width=165,
                            tag='pipeline',
                            callback=save_setting,
                        )
                        for pipeline, details in hinter.settings.pipelines.items():
                            safe_name = pipeline.replace(' ', '_').replace(',', '').lower()
                            hinter.imgui.add_text(
                                details['description'],
                                tag=f'pipeline_description-{safe_name}',
                                show=hinter.settings.pipeline == pipeline,
                            )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_checkbox(label='Enable Telemetry', default_value=False)

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=5)

                with hinter.imgui.table_row():
                    hinter.imgui.add_text(
                        '''If enabled, MobaHinted will send anonymous usage data to the developer.
Only the owning developer has access to the data, and the data is only
relevant to improving the application.''',
                        wrap=-1,
                    )

                with hinter.imgui.table_row():
                    with hinter.imgui.group(horizontal=True):
                        hinter.imgui.add_text('To see what data would be provided, look here:')
                        hinter.imgui.add_button(label='Telemetry Overview')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)
                with hinter.imgui.table_row():
                    hinter.imgui.add_separator()
                    hinter.imgui.add_spacer(height=20)
                # endregion Privacy Section

                # region Help Section
                with hinter.imgui.table_row():
                    hinter.imgui.add_text('Help')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_button(label='Package Logs')
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_button(label='Report an issue')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_button(label='Clear and Reload game Data')
                with hinter.imgui.table_row():
                    hinter.imgui.add_button(label='Clear MobaHinted item/rune pages')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_button(label='Clear all auto-generated item/rune pages')

                with hinter.imgui.table_row():
                    hinter.imgui.add_text(
                        'This will remove all item/rune pages labelled as MobaHinted/Blitz/etc.'
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_button(label='Reset MobaHinted')

                with hinter.imgui.table_row():
                    hinter.imgui.add_text(
                        '''This will remove all item/rune pages labelled as MobaHinted, default
all MobaHinted settings, clear all accounts tracked in MobaHinted, and
clear all game data MobaHinted cached.'''
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)
                with hinter.imgui.table_row():
                    hinter.imgui.add_separator()
                    hinter.imgui.add_spacer(height=20)
                # endregion Help Section

                # region About Section
                with hinter.imgui.table_row():
                    hinter.imgui.add_text('About')

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    # noinspection SpellCheckingInspection
                    hinter.imgui.add_text(
                        '''Made by zbee, mostly in season 13.
Copyright 2020 Ethan Henderson. Available under the GPLv3 license.
Open Source at github.com/zbee/mobahinted'''
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_text('League Patch:')
                    hinter.imgui.add_text(cassiopeia.get_version(region=hinter.settings.region))
                    hinter.imgui.add_text('MobaHinted Ver.:')
                    hinter.imgui.add_text(hinter.settings.version)

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_button(label='View Changelog', width=-1)
                    hinter.imgui.add_button(label='Check for Update', width=-1)

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=20)

                with hinter.imgui.table_row():
                    hinter.imgui.add_button(
                        label='Support the Project',
                        width=570,
                        callback=lambda: webbrowser.open('https://paypal.me/zbee0'),
                    )
                # endregion About Section

    def add_menu_separator(self, parent: str = 0):
        # Simply adding a separator to the menu via a disabled, empty menu item
        hinter.imgui.add_menu_item(label='', parent=parent, enabled=False)

    def new_screen(self, tag: str, set_primary: bool = False):
        # Set the new window as the primary window when ready
        if set_primary:
            hinter.imgui.set_primary_window(window=tag, value=True)
            return

        if hinter.imgui.does_item_exist(tag):
            # Empty the old window
            self.clear_screen()
        else:
            # Add a new window
            hinter.imgui.add_window(tag=tag)

        # Save the new window tag
        self.screen = tag

        # Add the menu bar back
        self.render_frames()
        self.add_menu()

    def clear_screen(self):
        hinter.imgui.delete_item(item=self.screen, children_only=True)

    def get_center(self, window: str = None):
        if window is not None:
            window = self.screen

        window_size = hinter.imgui.get_item_rect_size(window)
        window_size[0] = int(window_size[0] / 2)
        window_size[1] = int(window_size[1] / 2)

        return window_size

    def center_window(self, window: str, static_size: list[int] = None, parent: str = None):
        hinter.imgui.split_frame()

        # Get the center of the window to be centered
        if static_size is not None:  # Overwrite with provided values if needed
            this_window_size = static_size
        else:
            this_window_size = hinter.imgui.get_item_rect_size(window)

        this_window_size[0] = int(this_window_size[0] / 2)
        this_window_size[1] = int(this_window_size[1] / 2)

        # Default the parent (to center inside) to the screen
        if parent is None:
            parent = self.screen

        # Get the center of the parent window
        app_size = hinter.imgui.get_item_rect_size(parent)
        app_size[0] = int(app_size[0] / 2)
        app_size[1] = int(app_size[1] / 2)

        # Set the position of the window to center
        hinter.imgui.set_item_pos(
            window,
            [
                app_size[0] - this_window_size[0],
                app_size[1] - this_window_size[1]
            ]
        )

        hinter.imgui.split_frame()

    def render_frames(self, frames: int = 1, split: bool = False):
        if split:
            hinter.imgui.split_frame(delay=frames)

        for _ in range(frames):
            hinter.imgui.render_dearpygui_frame()

    def load_image(self,
                   image_name: str,
                   image_type: str = None,
                   image: Union[str, Image.Image] = None,
                   crop: tuple[int, int, int, int] = None,
                   size: tuple[int, int] = None,
                   force_fresh: bool = False) -> str:
        """A method to load an image, for use in :func:`dearpygui.add_image`.

        This accepts several different types of images, loads them however they need loaded, caches them, adds
        them to the dearpygui texture registry, and returns a texture tag to use in :func:`dearpygui.add_image`.

        .. warning::
            This method does not handle unregistering textures, that should be done manually.

        :param image_name: A unique name for the image, to be used to name the texture. If this is the only parameter,
            then the image must already exist in the cache.
        :param image_type: (Optional, requires an image) A constant from hinter.UI specifying the type of image you are
            providing.
        :param image: (Optional, requires a type) An image matching the type specified.
        :param crop: (Optional) A tuple of 4 integers specifying the crop area (x, y, width, height).
        :param size: (Optional) A tuple of 2 integers specifying the size the final image should be (width, height).
        :param force_fresh: (Optional) A boolean specifying whether to force a fresh load of the image.
        :return: A string specifying the texture tag to use in :func:`dearpygui.add_image`.

        .. seealso::
            :func:`hinter.UI.PIL`, :func:`hinter.UI.FILE`, :func:`hinter.UI.REMOTE`

            :func:`PIL.Image.crop`, :func:`PIL.Image.resize`

            :func:`dearpygui.add_image`, :func:`dearpygui.add_raw_texture`

            Originally based on code from `this DearPyGui discord Post
            <https://discord.com/channels/736279277242417272/1142743334402674688>`_

        :Example:

        .. code-block:: python
            img = self.ui.load_image(hinter.data.constants.IMAGE_TYPE_PIL, '/path/to/img', size=(64, 64))
            self.ui.imgui.add_image(texture_tag=img)
        """
        img: Image
        image_path = f'{hinter.data.constants.PATH_IMAGES}{image_name}.png'
        tag = f'CACHED_IMAGE-{image_name}'
        cached = False

        # Short-circuit if the image is already loaded into the registry
        if hinter.imgui.does_alias_exist(tag) and not force_fresh:
            return tag

        # Verify folder exists
        if not os.path.exists(hinter.data.constants.PATH_IMAGES):
            os.mkdir(hinter.data.constants.PATH_IMAGES)

        # Load the image if it is already cached
        if os.path.exists(image_path) and not force_fresh:
            image_type = hinter.data.constants.IMAGE_TYPE_FILE
            image = image_path
            cached = True

        if image_type == hinter.data.constants.IMAGE_TYPE_PIL:
            img = image
        elif image_type == hinter.data.constants.IMAGE_TYPE_FILE:
            img = Image.open(image)
        elif image_type == hinter.data.constants.IMAGE_TYPE_REMOTE:
            img = Image.open(requests.get(image, stream=True).raw)
        else:
            print('hinter.UI: Cannot load image with un-handled type', image_name, image_type, image)
            return self.filler_image

        # Crop if necessary
        if crop is not None and not cached:
            img = img.crop(crop)

        # Cache the image
        if not cached:
            img.save(image_path)

        # Resize if desired
        if size is not None:
            img = img.resize(size)

        # Create the texture from the image
        texture = img.convert('RGBA')
        height_, width_, __ = np.shape(img)

        texture = np.true_divide(
            np.asarray(
                np.array(texture).ravel(),
                dtype='f'),
            255.0
        )

        # Add the texture to the registry
        hinter.imgui.add_raw_texture(
            tag=tag,
            width=width_,
            height=height_,
            default_value=texture,
            format=hinter.imgui.mvFormat_Float_rgba,
            parent='images',
        )

        return tag

    # noinspection PyMethodMayBeStatic
    def check_image_cache(self, image_name: str) -> bool:
        """A method to check if an image is cached.

        :param image_name: The name of the image to check.
        :return: A boolean specifying whether the image is cached.
        """
        return os.path.exists(f'{hinter.data.constants.PATH_IMAGES}{image_name}.png')

    def text_size(self, text: Union[str, int], font: str, padding: Union[list[int], None] = None) -> list[int]:
        """A method to get the size of a string as displayed by ImGUI

        :param text: The text to get the size of, or a number of characters to get the size of.
        :param font: The font to use to calculate the size.
        :param padding: (Optional) The amount of padding to add to the size.
        :return: A tuple of 2 integers specifying the size of the text (width, height).
        """
        # Default padding is 0,0
        if padding is None:
            padding = [0, 0]

        # Set text to a number of characters, if requested
        if isinstance(text, int):
            text = 'a' * text

        # Grab the text size
        text_size = hinter.imgui.get_text_size(
            text,
            font=font,
        )

        # Account for the font scale and padding
        scale = 1 / hinter.data.constants.UI_FONT_SCALE
        return [
            int(text_size[0] * scale) + padding[0],
            int(text_size[1] * scale) + padding[1],
        ]

    def exit_callback(self):
        window_position = hinter.imgui.get_viewport_pos()

        if hinter.settings.save_window_position:
            hinter.settings.write_setting('x', window_position[0])
            hinter.settings.write_setting('y', window_position[1])

            hinter.settings.write_setting('width', hinter.imgui.get_viewport_width())
            hinter.settings.write_setting('height', hinter.imgui.get_viewport_height())

    def imgui_init(self, save: bool = False):
        """Method to load or save ImGUI's init file

        This method first ensures the init file exists, then either loads or saves it.

        .. warning::
            Loading should only be handled in the UI class

        :param save: Whether we are saving or loading an init file
        """
        saving = save
        init_file = hinter.data.constants.PATH_IMGUI_FILE

        # Make the directory and file as needed
        if not os.path.exists(init_file):
            open(init_file, 'w+')
            # Don't load a brand new, empty file
            return

        # Don't try to load an empty file
        elif os.stat(init_file).st_size == 0 and not saving:
            return

        if not saving:
            hinter.imgui.configure_app(init_file=init_file, load_init_file=True)
        else:
            hinter.imgui.save_init_file(init_file)

    def error_screens(self, error):
        if hinter.imgui.does_item_exist('login'):
            hinter.imgui.delete_item('login')

        if hinter.imgui.does_item_exist('loading'):
            hinter.imgui.delete_item('loading')

        hinter.imgui.set_viewport_min_width(350)
        hinter.imgui.set_viewport_width(350)
        hinter.imgui.set_viewport_min_height(600)
        hinter.imgui.set_viewport_height(600)

        if '503' in str(error):
            region = cassiopeia.Region(hinter.settings.region)
            platform = cassiopeia.Platform[region.name].value.lower()

            with hinter.imgui.window(tag='error'):
                hinter.imgui.add_spacer(height=150)

                text = 'Riot services are unavailable.'
                hinter.imgui.add_text(f'{text:^40}')
                text = 'Please try later.'
                hinter.imgui.add_text(f'{text:^40}')

                hinter.imgui.add_spacer(height=40)

                text = 'You can check the LoL status page:'
                hinter.imgui.add_text(f'{text:^40}')
                hinter.imgui.add_button(
                    label='Open status.rito Page',
                    callback=lambda: webbrowser.open(f'https://status.riotgames.com/lol?region={platform}'),
                    width=-1,
                )
                text = '(rarely posted if issues are unexpected)'
                hinter.imgui.add_text(f'{text:^40}')

            hinter.imgui.set_primary_window('error', True)
            hinter.imgui.start_dearpygui()
            self.exit_callback()
            exit(503)
        elif '403' in str(error):
            with hinter.imgui.window(tag='error'):
                hinter.imgui.add_spacer(height=175)
                text = 'This API key is invalid or expired.'
                hinter.imgui.add_text(f'{text:^40}')
                text = 'Please enter a new one.'
                hinter.imgui.add_text(f'{text:^40}')

                hinter.imgui.add_spacer(height=20)

                text = 'You can get a new one here:'
                hinter.imgui.add_text(f'{text:^40}')
                hinter.imgui.add_button(
                    label='Open developer.rito Page',
                    callback=lambda: webbrowser.open('https://developer.riotgames.com'),
                    width=-1,
                )

            hinter.imgui.set_primary_window('error', True)
            hinter.imgui.start_dearpygui()
            self.exit_callback()
            exit(403)
        else:
            print(error)
            exit('unknown error')
