import os.path

import cassiopeia
import dearpygui.dearpygui

import hinter.users


# noinspection PySimplifyBooleanCheck
class Settings:
    settings_file = './data/settings.dat'
    region = 'NA'
    active_user = ''
    settings_loaded = False
    version = '0.0.0'
    imgui = dearpygui.dearpygui
    x: int = 10  # Window Position
    y: int = 10

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
            # TODO: this delays the program starting, likely because it's all run-time adding. Run this in UI.__init__?

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
                    self.imgui.add_combo(items=[e.username for e in users], default_value=self.active_user, width=-1)
                    self.imgui.add_text('Current Region:')
                    self.imgui.add_combo(
                        items=[e.value for e in cassiopeia.data.Region],
                        default_value=self.region,
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
                            default_value=self.region,
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
                    self.imgui.add_text(cassiopeia.get_version(region=self.region))
                    self.imgui.add_text('Mobahinted Ver.:')
                    self.imgui.add_text(self.version)

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

    def load_settings(self, refresh: bool = False):
        # Skip loading of settings if they are already loaded
        if not refresh and self.settings_loaded:
            print('hinter.Settings: settings already loaded')
            return

        # Verify folder and file exist
        if not os.path.exists('./data/'):
            os.mkdir('./data')
        if not os.path.exists(self.settings_file):
            open(self.settings_file, 'w+')
            return

        # Open settings file
        settings_file = open(self.settings_file, 'r').readlines()

        # Read settings file
        for setting in settings_file:
            # Skip blank lines
            if setting == '\n':
                continue

            # Read the setting into variables
            setting = setting.split('=')
            attribute = setting[0]
            value = setting[1].split('\n')[0]

            # Save the setting to the Class
            # This has to be verbose otherwise falsey values will trip it
            if getattr(self, attribute, False) != False:
                setattr(self, attribute, value)

        # Save a setting that the settings were loaded
        self.settings_loaded = True

    def write_setting(self, setting, value):
        # Verify folder and file exist
        if not os.path.exists('./data/'):
            os.mkdir('./data')
        if not os.path.exists(self.settings_file):
            open(self.settings_file, 'w+')
            return

        # Remove the setting if currently set
        # This has to be verbose otherwise falsey values will trip it
        if getattr(self, setting, False) != False:
            settings_file_original = open(self.settings_file, 'r').readlines()
            lines = []

            # Go through list
            for line in settings_file_original:
                # Skip blank lines
                if line == '\n':
                    continue

                # Check setting in list
                setting_name = line.split('=')[0]
                # If the setting name matches the one wanting updated
                # then don't record it
                if setting_name == setting:
                    removed = True
                else:
                    lines.append(line)

            # Reopen file with write permissions
            settings_file = open(self.settings_file, 'w+')

            # Write all the recorded lines
            for line in lines:
                settings_file.write(line)

            settings_file.close()

        # Add the setting
        settings_file = open(self.settings_file, 'a+')
        settings_file.write(f'{setting}={value}\n')
        settings_file.close()

        # Reload settings file
        self.load_settings(refresh=True)
