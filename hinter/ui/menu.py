import hinter
import cassiopeia
import webbrowser


class UIMenus:

    def __init__(self, ui):
        self.ui = ui

    def add_menu(self):
        # Delete the old menu bar, if it exists, and add a new one
        if hinter.imgui.does_item_exist('menu'):
            hinter.imgui.delete_item(item='menu')

        with hinter.imgui.menu_bar(tag='menu', parent=self.ui.screen):
            # region Settings Menu
            hinter.imgui.add_menu_item(
                label='Settings',
                callback=lambda: (
                    hinter.imgui.show_item(item='settings-popup'),
                    self.ui.center_window('settings-popup'),
                ),
            )
            self.ready_settings_window()
            # endregion Settings Menu

            # region Data Menu
            with hinter.imgui.menu(label='Data', tag='menu-data'):
                hinter.imgui.add_menu_item(
                    label='Reload all data',
                    parent='menu-data',
                    callback=lambda: self.ui.data_loader.load_all(refresh=True)
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
                users = hinter.users.list_users(self.ui.screen)
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
                            self.ui.move_on_callback(ui=self, render=not self.ui.render),
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
        settings_gear = self.ui.load_image(
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

    # noinspection PyMethodMayBeStatic
    def add_menu_separator(self, parent: str = 0):
        # Simply adding a separator to the menu via a disabled, empty menu item
        hinter.imgui.add_menu_item(label='', parent=parent, enabled=False)
