import os
from typing import Union

import PIL.Image as Image
import dearpygui.dearpygui
import numpy as np
import requests
import cassiopeia

import hinter
import hinter.background.dataloader
import hinter.struct.user

FONT_SCALE = 2


class UI:
    imgui: dearpygui.dearpygui = dearpygui.dearpygui
    screen: str = 'login'
    font: dict = {
        'regular': None,
        'medium': None,
        'bold': None,
    }
    PIL = 'pil'
    FILE = 'file'
    REMOTE = 'remote'
    user_available: bool = False
    data_loader: hinter.background.dataloader.DataLoader
    filler_image: str
    move_on_callback: callable
    render: bool
    data_loader: hinter.background.dataloader.DataLoader

    def __init__(self, move_on_callback):
        self.move_on_callback = move_on_callback
        self.imgui.create_context()
        self.imgui_init()

        # Set up Fira Code for use
        with self.imgui.font_registry():
            self.font['regular'] = self.imgui.add_font('./assets/fcr.ttf', 16 * FONT_SCALE)
            self.font['medium'] = self.imgui.add_font('./assets/fcm.ttf', 16 * FONT_SCALE)
            self.font['bold'] = self.imgui.add_font('./assets/fcb.ttf', 16 * FONT_SCALE)
            self.font['24 regular'] = self.imgui.add_font('./assets/fcr.ttf', 24 * FONT_SCALE)
            self.font['24 medium'] = self.imgui.add_font('./assets/fcm.ttf', 24 * FONT_SCALE)
            self.font['24 bold'] = self.imgui.add_font('./assets/fcb.ttf', 24 * FONT_SCALE)
            self.font['32 regular'] = self.imgui.add_font('./assets/fcr.ttf', 32 * FONT_SCALE)
            self.font['32 medium'] = self.imgui.add_font('./assets/fcm.ttf', 32 * FONT_SCALE)
            self.font['32 bold'] = self.imgui.add_font('./assets/fcb.ttf', 32 * FONT_SCALE)
            self.font['40 regular'] = self.imgui.add_font('./assets/fcr.ttf', 40 * FONT_SCALE)
            self.font['40 medium'] = self.imgui.add_font('./assets/fcm.ttf', 40 * FONT_SCALE)
            self.font['40 bold'] = self.imgui.add_font('./assets/fcb.ttf', 40 * FONT_SCALE)
            self.font['48 regular'] = self.imgui.add_font('./assets/fcr.ttf', 48 * FONT_SCALE)
            self.font['48 medium'] = self.imgui.add_font('./assets/fcm.ttf', 48 * FONT_SCALE)
            self.font['48 bold'] = self.imgui.add_font('./assets/fcb.ttf', 48 * FONT_SCALE)
            self.font['56 regular'] = self.imgui.add_font('./assets/fcr.ttf', 56 * FONT_SCALE)
            self.font['56 medium'] = self.imgui.add_font('./assets/fcm.ttf', 56 * FONT_SCALE)
            self.font['56 bold'] = self.imgui.add_font('./assets/fcb.ttf', 56 * FONT_SCALE)
        self.imgui.set_global_font_scale(1 / FONT_SCALE)
        self.imgui.bind_font(self.font['medium'])

        self.imgui.setup_dearpygui()

        self.imgui.add_texture_registry(tag='images')

        self.imgui.create_viewport(
            # decorated=False, # Would have to add manual resizing, maximizing, etc
            title='MobaHinted',
            min_width=350,
            width=350,
            min_height=600,
            height=600,
            small_icon='./assets/logo.ico',
            large_icon='./assets/logo.ico',
            x_pos=int(hinter.settings.x),
            y_pos=int(hinter.settings.y),
        )
        self.imgui.set_exit_callback(self.exit_callback)

        self.filler_image = self.load_image('filler', self.FILE, './assets/filler.png', size=(1, 1))

        # region Login flow
        def login_submit():
            username = self.imgui.get_value('add-username')
            region = self.imgui.get_value('add-region')

            hinter.settings.write_setting('region', region)
            added = hinter.users.add_user(ui=self, username=username)

            if added:
                self.user_available = True
                hinter.settings.write_setting('active_user', username)
                self.data_loader = hinter.background.dataloader.DataLoader()
                self.render = False
                move_on_callback(ui=self, render=self.render)
                self.imgui.render_dearpygui_frame()

        if hinter.settings.active_user == '':
            with self.imgui.window(tag=self.screen):
                with self.imgui.table(header_row=False):
                    self.imgui.add_table_column(init_width_or_weight=0.15)
                    self.imgui.add_table_column(init_width_or_weight=0.7)
                    self.imgui.add_table_column(init_width_or_weight=0.15)

                    with self.imgui.table_row():
                        self.imgui.add_spacer()
                        self.imgui.add_spacer(height=150)
                        self.imgui.add_spacer()

                    with self.imgui.table_row():
                        self.imgui.add_spacer()
                        self.imgui.add_text('Add your League Account')
                        self.imgui.add_spacer()

                    with self.imgui.table_row():
                        self.imgui.add_spacer(height=10)

                    with self.imgui.table_row():
                        self.imgui.add_spacer()
                        self.imgui.add_input_text(
                            tag='add-username',
                            hint='League Name',
                            width=-1,
                            on_enter=True,
                            callback=login_submit,
                        )

                    with self.imgui.table_row():
                        self.imgui.add_spacer()
                        with self.imgui.group(horizontal=True):
                            self.imgui.add_text('Region: ')
                            self.imgui.add_combo(
                                tag='add-region',
                                items=[e.value for e in cassiopeia.data.Region],
                                default_value=hinter.settings.region,
                                width=-1,
                                callback=login_submit,
                            )

                    with self.imgui.table_row():
                        self.imgui.add_spacer(height=10)

                    with self.imgui.table_row():
                        self.imgui.add_spacer()
                        self.imgui.add_button(
                            tag='add-button',
                            label='Add >',
                            width=-1,
                            callback=login_submit,
                        )

            self.imgui.set_primary_window(window=self.screen, value=True)
            self.imgui.show_viewport()
            self.imgui.set_viewport_resizable(False)
        # endregion Login flow
        else:
            self.user_available = True
            self.screen = 'loading'

            with self.imgui.window(tag=self.screen):
                with self.imgui.table(header_row=False):
                    self.imgui.add_table_column()
                    self.imgui.add_table_column()
                    self.imgui.add_table_column()

                    with self.imgui.table_row():
                        self.imgui.add_spacer()
                        self.imgui.add_spacer(height=250)
                        self.imgui.add_spacer()

                    with self.imgui.table_row():
                        self.imgui.add_spacer()
                        self.imgui.add_text('Loading')
                        self.imgui.add_spacer()

                    with self.imgui.table_row():
                        self.imgui.add_spacer()
                        self.imgui.add_loading_indicator()
                        self.imgui.add_spacer()

            self.data_loader = hinter.background.dataloader.DataLoader()
            self.imgui.set_primary_window(window=self.screen, value=True)
            self.imgui.show_viewport()
            self.render_frames(120)
            self.render = True
            move_on_callback(ui=self, render=self.render)

    def show_info_popup(self, title: str, text: str, width: int = 225, height: int = 125):
        # Wait one frame to ensure that other modals are closed
        self.imgui.split_frame()

        # Ensure the popup can close itself
        def close_popup():
            self.imgui.delete_item(item='info-popup')
            self.imgui.delete_item(item='info-text')
            self.imgui.delete_item(item='info-spacer')
            self.imgui.delete_item(item='info-ok')

        # Show the popup
        with self.imgui.window(
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
            self.imgui.add_text(tag='info-text', default_value=text, wrap=width - 20)

            # Button to close the popup
            self.imgui.add_spacer(tag='info-spacer', height=10)
            self.imgui.add_button(
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
        if self.imgui.does_item_exist('menu'):
            self.imgui.delete_item(item='menu')

        with self.imgui.menu_bar(tag='menu', parent=self.screen):
            # region Settings Menu
            self.imgui.add_menu_item(
                label='Settings',
                callback=lambda: (
                    self.imgui.show_item(item='settings-popup'),
                    self.center_window('settings-popup'),
                ),
            )
            self.ready_settings_window()
            # endregion Settings Menu

            # region Data Menu
            with self.imgui.menu(label='Data', tag='menu-data'):
                self.imgui.add_menu_item(
                    label='Reload all data',
                    parent='menu-data',
                    callback=lambda: self.data_loader.load_all(refresh=True)
                )
            # endregion Data Menu

            # region User Menu
            with self.imgui.menu(label='User', tag='menu-user'):
                # Option to add a user
                self.imgui.add_menu_item(
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
                    self.imgui.add_menu_item(
                        tag=f'menu-user-{username}',
                        label=username,
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
                    self.imgui.add_menu_item(
                        label='Remove User',
                        callback=lambda: (hinter.users.remove_user(self)),
                    )
            # endregion User Menu

            # region Help Menu
            with self.imgui.menu(label='Help', tag='menu-help'):
                self.imgui.add_menu_item(
                    label='Quick Guide',
                    callback=lambda: (),
                )

                self.add_menu_separator()

                self.imgui.add_menu_item(
                    label='Offer Feedback',
                    callback=lambda: (),
                )

                self.imgui.add_menu_item(
                    label='Report an Issue',
                    callback=lambda: (),
                )

                self.imgui.add_menu_item(
                    label='Suggest a feature',
                    callback=lambda: (),
                )

                self.add_menu_separator()

                self.imgui.add_menu_item(
                    label='Contribute Code',
                    callback=lambda: (),
                )
            # endregion About Menu

            # region About Menu
            with self.imgui.menu(label='About', tag='menu-about'):

                self.imgui.add_menu_item(
                    label='''Made by zbee, mostly in season 13
Copyright 2020 Ethan Henderson
Available under the GPLv3 license
Open Source at github.com/zbee/mobahinted''',
                    enabled=False,
                )
            # endregion About Menu

    def ready_settings_window(self):
        if self.imgui.does_item_exist(item='settings-popup'):
            return

        # Make sure the popup can be hidden
        def close_popup():
            self.imgui.hide_item(item='settings-popup')

        # Show the popup
        with self.imgui.window(
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

            with self.imgui.table(header_row=False, no_clip=True):
                self.imgui.add_table_column()
                self.imgui.add_table_column()
                self.imgui.add_table_column()
                self.imgui.add_table_column()

                # region Overlay Section
                with self.imgui.table_row():
                    self.imgui.add_text('Overlays')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Milestone Notifications',
                        default_value=False,
                    )
                    self.imgui.add_spacer()
                    self.imgui.add_checkbox(
                        label='CS Tracker and Stats Window',
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Objective Reminders',
                        default_value=False,
                    )
                    self.imgui.add_spacer()
                    self.imgui.add_checkbox(
                        label='Enemy Spell Tracker',
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Jungle Timers',
                        default_value=False,
                    )
                    self.imgui.add_spacer()
                    self.imgui.add_checkbox(
                        label='ARAM Health Timers',
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Scoreboard Duos",
                        default_value=False,
                    )
                    self.imgui.add_spacer()
                    self.imgui.add_checkbox(
                        label="Gold Diff Tracker",
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    with self.imgui.group(horizontal=True):
                        self.imgui.add_checkbox(
                            label='Map Check Reminder',
                            default_value=True,
                        )
                        self.imgui.add_button(label='G')
                        # TODO: Make this the assets/settings.png, and add it to all overlays
                    self.imgui.add_spacer()
                    self.imgui.add_checkbox(
                        label='Back Reminder',
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Use Trinket Reminder',
                        default_value=False,
                    )
                    self.imgui.add_spacer()
                    self.imgui.add_checkbox(
                        label='Counter Item Suggestions',
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_button(label='View all Overlay positions')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)
                with self.imgui.table_row():
                    self.imgui.add_separator()
                    self.imgui.add_spacer(height=20)
                # endregion Overlay Section

                # region Behavior Section
                with self.imgui.table_row():
                    self.imgui.add_text('Application Behavior')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Launch MobaHinted on system startup',
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Keep MobaHinted up to date automatically',
                        default_value=True,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Close MobaHinted to the tray',
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Bring MobaHinted to the front on window change',
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Always show MobaHinted in the same place',
                        default_value=True,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label='Detect new accounts automatically',
                        default_value=True,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Show my rank to me",
                        default_value=True,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Show teammate ranks",
                        default_value=True,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Show enemy ranks",
                        default_value=True,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Show game average ranks",
                        default_value=True,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Show the current-play-session window",
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Show pre-game/lobby info as a separate window",
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Show pre-game build suggestions as a separate window",
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Automatically close the pre-game build suggestions window",
                        default_value=True,
                        indent=25,
                    )

                with self.imgui.table_row():
                    self.imgui.add_checkbox(
                        label="Show post-game as a separate window",
                        default_value=False,
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_button(label='Customize Theme')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)
                with self.imgui.table_row():
                    self.imgui.add_separator()
                    self.imgui.add_spacer(height=20)
                # endregion Behavior Section

                # region Accounts Section
                with self.imgui.table_row():
                    self.imgui.add_text('Accounts')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_text('Current Account:')
                    self.imgui.add_combo(items=[e.username for e in users], default_value=hinter.settings.active_user, width=-1)
                    self.imgui.add_text('Current Region:')
                    self.imgui.add_combo(
                        items=[e.value for e in cassiopeia.data.Region],
                        default_value=hinter.settings.region,
                        width=60
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_text('Add an Account:')
                    self.imgui.add_input_text(hint='League Name', width=-1)
                    self.imgui.add_text('On Region:')
                    with self.imgui.group(horizontal=True):
                        self.imgui.add_combo(
                            items=[e.value for e in cassiopeia.data.Region],
                            default_value=hinter.settings.region,
                            width=60
                        )
                        self.imgui.add_button(label='Add >', width=-1)

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)
                with self.imgui.table_row():
                    self.imgui.add_separator()
                    self.imgui.add_spacer(height=20)
                # endregion Accounts Section

                # region Privacy Section
                with self.imgui.table_row():
                    self.imgui.add_text('Privacy')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_text('Current Data Pipeline:')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=10)

                with self.imgui.table_row():
                    pipeline = 'MHK,Cdragon'

                    if pipeline == 'MHK,Cdragon':
                        with self.imgui.group(horizontal=True):
                            self.imgui.add_combo(
                                items=[
                                    'Most Private',       # Riot dev key
                                    'Private, Accurate',  # Riot dev key and cdragon
                                    'Fast, Accurate',     # CDragon and MHK
                                ],
                                default_value='Fast, Accurate',
                                width=165,
                            )
                            self.imgui.add_text(': CommunityDragon > Mobahinted Proxy > Riot')
                    if pipeline == 'Dev Key':
                        with self.imgui.group(horizontal=True):
                            self.imgui.add_button(label='Mobahinted', enabled=False)
                            self.imgui.add_text('>')
                            self.imgui.add_button(label='Riot', enabled=False)

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_checkbox(label='Enable Telemetry', default_value=False)

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=5)

                with self.imgui.table_row():
                    self.imgui.add_text(
                        '''If enabled, Mobahinted will send anonymous usage data to the developer.
Only the owning developer has access to the data, and the data is only
relevant to improving the application.''',
                        wrap=-1,
                    )

                with self.imgui.table_row():
                    with self.imgui.group(horizontal=True):
                        self.imgui.add_text('To see what data would be provided, look here:')
                        self.imgui.add_button(label='Telemetry Overview')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)
                with self.imgui.table_row():
                    self.imgui.add_separator()
                    self.imgui.add_spacer(height=20)
                # endregion Privacy Section

                # region Help Section
                with self.imgui.table_row():
                    self.imgui.add_text('Help')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_button(label='Package Logs')
                    self.imgui.add_spacer()
                    self.imgui.add_spacer()
                    self.imgui.add_button(label='Report an issue')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_button(label='Clear and Reload game Data')
                with self.imgui.table_row():
                    self.imgui.add_button(label='Clear MobaHinted item/rune pages')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_button(label='Clear all auto-generated item/rune pages')

                with self.imgui.table_row():
                    self.imgui.add_text(
                        'This will remove all item/rune pages labelled as MobaHinted/Blitz/etc.'
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_button(label='Reset MobaHinted')

                with self.imgui.table_row():
                    self.imgui.add_text(
                        '''This will remove all item/rune pages labelled as MobaHinted, default
all MobaHinted settings, clear all added accounts, and clear all cached
game data.'''
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)
                with self.imgui.table_row():
                    self.imgui.add_separator()
                    self.imgui.add_spacer(height=20)
                # endregion Help Section

                # region About Section
                with self.imgui.table_row():
                    self.imgui.add_text('About')

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_text(
                        '''Made by zbee, mostly in season 13.
Copyright 2020 Ethan Henderson. Available under the GPLv3 license.
Open Source at github.com/zbee/mobahinted'''
                    )

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_text('League Patch:')
                    self.imgui.add_text(cassiopeia.get_version(region=hinter.settings.region))
                    self.imgui.add_text('Mobahinted Ver.:')
                    self.imgui.add_text(hinter.settings.version)

                with self.imgui.table_row():
                    self.imgui.add_spacer()
                    self.imgui.add_spacer()
                    self.imgui.add_button(label='View Changelog', width=-1)
                    self.imgui.add_button(label='Check for Update', width=-1)

                with self.imgui.table_row():
                    self.imgui.add_spacer(height=20)

                with self.imgui.table_row():
                    self.imgui.add_button(label='Support the Project', width=570)
                # endregion About Section

    def add_menu_separator(self, parent: str = 0):
        # Simply adding a separator to the menu via a disabled, empty menu item
        self.imgui.add_menu_item(label='', parent=parent, enabled=False)

    def new_screen(self, tag: str, set_primary: bool = False):
        # Set the new window as the primary window when ready
        if set_primary:
            self.imgui.set_primary_window(window=tag, value=True)
            return

        # Add a new window
        self.imgui.add_window(tag=tag)

        # Delete the old window
        self.imgui.delete_item(item=self.screen)

        # Save the new window tag
        self.screen = tag

        # Add the menu bar back
        self.add_menu()

    def clear_screen(self):
        self.imgui.delete_item(item=self.screen, children_only=True)

    def get_center(self, window: str = None):
        if window is not None:
            window = self.screen

        window_size = self.imgui.get_item_rect_size(window)
        window_size[0] = int(window_size[0] / 2)
        window_size[1] = int(window_size[1] / 2)

        return window_size

    def center_window(self, window: str, static_size: list[int] = None, parent: str = None):
        self.imgui.split_frame()

        # Get the center of the window to be centered
        if static_size is not None:  # Overwrite with provided values if needed
            this_window_size = static_size
        else:
            this_window_size = self.imgui.get_item_rect_size(window)

        this_window_size[0] = int(this_window_size[0] / 2)
        this_window_size[1] = int(this_window_size[1] / 2)

        # Default the parent (to center inside) to the screen
        if parent is None:
            parent = self.screen

        # Get the center of the parent window
        app_size = self.imgui.get_item_rect_size(parent)
        app_size[0] = int(app_size[0] / 2)
        app_size[1] = int(app_size[1] / 2)

        # Set the position of the window to center
        self.imgui.set_item_pos(
            window,
            [
                app_size[0] - this_window_size[0],
                app_size[1] - this_window_size[1]
            ]
        )

        self.imgui.split_frame()

    def render_frames(self, frames: int = 1, split: bool = False):
        if split:
            self.imgui.split_frame(delay=frames*10)

        for _ in range(frames):
            self.imgui.render_dearpygui_frame()

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
        :param force_fresh: (Optional) A boolean specifying whether or not to force a fresh load of the image.
        :return: A string specifying the texture tag to use in :func:`dearpygui.add_image`.

        .. seealso::
            :func:`hinter.UI.PIL`, :func:`hinter.UI.FILE`, :func:`hinter.UI.REMOTE`

            :func:`PIL.Image.crop`, :func:`PIL.Image.resize`

            :func:`dearpygui.add_image`, :func:`dearpygui.add_raw_texture`

            Originally based on code from `this DearPyGui discord Post
            <https://discord.com/channels/736279277242417272/1142743334402674688>`_

        :Example:

        .. code-block:: python
            img = self.ui.load_image(self.ui.PIL, '/path/to/img', size=[64, 64])
            self.ui.imgui.add_image(texture_tag=img)

        .. todo::
            Implement this method
            Unregister textures when they are no longer needed; clear_screen(), new_screen()?
        """
        img: Image
        image_path = f'./data/image_cache/{image_name}.png'
        tag = f'CACHED_IMAGE-{image_name}'
        cached = False

        # Short-circuit if the image is already loaded into the registry
        if self.imgui.does_alias_exist(tag) and not force_fresh:
            return tag

        # Verify folder exists
        if not os.path.exists('./data/image_cache/'):
            os.mkdir('./data/image_cache/')

        # Load the image if it is already cached
        if os.path.exists(image_path) and not force_fresh:
            image_type = self.FILE
            image = image_path
            cached = True

        if image_type == self.PIL:
            img = image
        elif image_type == self.FILE:
            img = Image.open(image)
        elif image_type == self.REMOTE:
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
        self.imgui.add_raw_texture(
            tag=tag,
            width=width_,
            height=height_,
            default_value=texture,
            format=self.imgui.mvFormat_Float_rgba,
            parent='images',
        )

        return tag

    # noinspection PyMethodMayBeStatic
    def check_image_cache(self, image_name: str) -> bool:
        """A method to check if an image is cached.

        :param image_name: The name of the image to check.
        :return: A boolean specifying whether the image is cached.
        """
        return os.path.exists(f'./data/image_cache/{image_name}.png')

    def exit_callback(self):
        window_position = self.imgui.get_viewport_pos()

        hinter.settings.write_setting('x', window_position[0])
        hinter.settings.write_setting('y', window_position[1])

    def imgui_init(self, save: bool = False):
        """Method to load or save ImGUI's init file

        This method first ensures the init file exists, then either loads or saves it.

        .. warning::
            Loading should only be handled in the UI class

        :param save: Whether we are saving or loading an init file
        """
        saving = save
        init_file = './data/imgui.ini'

        # Make the directory and file as needed
        if not os.path.exists('./data/'):
            os.mkdir('./data')
        if not os.path.exists(init_file):
            open(init_file, 'w+')
            # Don't load a brand new, empty file
            return

        # Don't try to load an empty file
        elif os.stat(init_file).st_size == 0 and not saving:
            return

        if not saving:
            self.imgui.configure_app(init_file=init_file, load_init_file=True)
        else:
            self.imgui.save_init_file(init_file)
