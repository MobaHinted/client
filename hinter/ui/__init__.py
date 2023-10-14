#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import os
import cassiopeia
import hinter


class UI:
    screen: str
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

    def loading(self):
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

        self.data_loader = hinter.DataLoader.DataLoader()
        hinter.imgui.set_primary_window(window=self.screen, value=True)
        hinter.imgui.show_viewport()
        hinter.imgui.render_dearpygui_frame()
        self.render = True
        self.move_on_callback(render=self.render)

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

        hinter.imgui.set_primary_window(window=self.screen, value=True)
        hinter.imgui.show_viewport()
        hinter.imgui.set_viewport_resizable(False)

    def _login(self):
        username = hinter.imgui.get_value('add-username')
        region = hinter.imgui.get_value('add-region')

        hinter.settings.write_setting('region', region)
        added = hinter.users.add_user(ui=self, username=username)

        if added:
            self.user_available = True
            hinter.settings.write_setting('active_user', username)
            self.data_loader = hinter.DataLoader.DataLoader()
            self.render = False
            self.move_on_callback(render=self.render)
            hinter.imgui.render_dearpygui_frame()
