#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import threading
import cassiopeia
import hinter


class UI:
    screen: str = ''
    font: dict
    move_on_callback: callable
    user_available: bool
    render: bool
    data_loader: hinter.DataLoader.DataLoader

    def __init__(self, move_on_callback: callable):
        self.move_on_callback = move_on_callback

        hinter.imgui.create_context()
        self.imgui_init()

        self.user_available = False
        self.font = {}

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

        hinter.UI = self

        if hinter.settings.active_user == '':
            self.login_flow()
        else:
            self.loading()

    # noinspection PyMethodMayBeStatic
    def exit_callback(self):
        window_position = hinter.imgui.get_viewport_pos()

        if hinter.settings.save_window_position:
            hinter.settings.write_setting('x', window_position[0])
            hinter.settings.write_setting('y', window_position[1])

            hinter.settings.write_setting('width', hinter.imgui.get_viewport_width())
            hinter.settings.write_setting('height', hinter.imgui.get_viewport_height())

    # noinspection PyMethodMayBeStatic
    def imgui_init(self, save: bool = False):
        """Method to load or save ImGUI's init file

        This method first ensures the init file exists, then either loads or saves it.

        .. warning::
            Loading should only be handled in the UI class

        :param save: Whether we are saving or loading an init file
        """
        saving = save
        init_file = hinter.data.constants.PATH_IMGUI_FILE

        # Don't try to load an empty file
        if hinter.data.management.file_empty(init_file) and not saving:
            return

        if not saving:
            hinter.imgui.configure_app(init_file=init_file, load_init_file=True)
        else:
            hinter.imgui.save_init_file(init_file)

    def loading(self, render: bool = True):
        from_login = False
        if self.screen == 'login':
            from_login = True

        self.user_available = True
        self.screen = 'loading'
        self.render = render

        # Make sure we can draw this screen
        if hinter.imgui.does_item_exist('login'):
            hinter.imgui.delete_item('login')
        if hinter.imgui.does_item_exist('loading'):
            hinter.imgui.delete_item('loading')

        # Set up the loading window, with centered loading spinner
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
                    if not from_login:
                        hinter.imgui.add_text('Loading')
                    else:
                        hinter.imgui.add_text('Downloading')
                    hinter.imgui.add_spacer()

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_loading_indicator()
                    hinter.imgui.add_spacer()

        hinter.imgui.set_primary_window(window=self.screen, value=True)
        if not from_login:
            hinter.imgui.show_viewport()
            hinter.imgui.set_viewport_resizable(False)

        # Load data
        def load_data():
            self.data_loader = hinter.DataLoader.DataLoader()

            thread = threading.Thread(target=self.move_on_callback)
            thread.start()
        thread = threading.Thread(target=load_data)
        thread.start()

    def login_flow(self):
        self.screen = 'login'
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

                # TODO: Update to searching by Riot IDs

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_input_text(
                        tag='add-username',
                        hint='League Name',
                        width=-1,
                        on_enter=True,
                        callback=self._login,
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
                            callback=self._login,
                        )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer(height=10)

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_button(
                        tag='add-button',
                        label='Add >',
                        width=-1,
                        callback=self._login,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer()
                    hinter.imgui.add_text(
                        tag='add-error',
                        default_value='',
                        color=hinter.data.constants.TEAM_RED_COLOR,
                    )

                with hinter.imgui.table_row():
                    hinter.imgui.add_spacer()
                    # Center the loading indicator
                    with hinter.imgui.table(header_row=False):
                        hinter.imgui.add_table_column()
                        hinter.imgui.add_table_column()
                        hinter.imgui.add_table_column()

                        with hinter.imgui.table_row():
                            hinter.imgui.add_spacer()
                            hinter.imgui.add_loading_indicator(tag='add-loading', show=False)

        hinter.imgui.set_primary_window(window=self.screen, value=True)
        hinter.imgui.show_viewport()
        hinter.imgui.set_viewport_resizable(False)

    def _login(self):
        # Load the values from the UI
        username = hinter.imgui.get_value('add-username')
        region = hinter.imgui.get_value('add-region')

        # Save the region specified
        hinter.settings.write_setting('region', region)

        # Show the spinner and reset the error to nothing
        hinter.imgui.show_item('add-loading')
        hinter.imgui.set_value('add-error', '')

        # Function to try to add the user
        def try_adding_user(username: str):
            added = hinter.users.add_user(username=username, show_popups=False)

            # Successfully added the user
            if added == 0:
                hinter.settings.write_setting('active_user', username)
                hinter.imgui.hide_item('add-loading')
                self.loading(render=False)
            else:
                # Showing errors from adding the user
                if added == 1:
                    hinter.imgui.set_value('add-error', 'This username is not valid')
                elif added == 2:
                    hinter.imgui.set_value('add-error', 'Account already in list')
                elif added == 3:
                    hinter.imgui.set_value('add-error', 'Account not found in region')
                else:
                    hinter.imgui.set_value('add-error', 'Unknown error')

                hinter.imgui.hide_item('add-loading')

        # Run the function in a thread
        thread = threading.Thread(target=try_adding_user, args=(username,))
        thread.start()
