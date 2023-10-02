import os
from typing import Union

import PIL.Image as Image
import dearpygui.dearpygui
import numpy as np
import requests

import hinter
import hinter.background.dataloader
import hinter.matchhistory
import hinter.struct.user

FONT_SCALE = 2


class UI:
    imgui: dearpygui.dearpygui = dearpygui.dearpygui
    screen: str = 'Login'
    font: dict = {
        'regular': None,
        'medium': None,
        'bold': None,
    }
    PIL = 'pil'
    FILE = 'file'
    REMOTE = 'remote'

    def __init__(self):
        self.imgui.create_context()

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
            min_width=300,
            width=300,
            min_height=600,
            height=600,
            small_icon='./assets/logo.ico',
            large_icon='./assets/logo.ico',
        )

        if hinter.settings.active_user == '':
            self.imgui.add_window(tag=self.screen)

            self.imgui.add_text('Login', parent=self.screen)

            self.imgui.set_viewport_resizable(False)
        else:
            self.screen = 'loading'
            self.imgui.add_window(tag=self.screen)
            self.add_menu()
            self.imgui.add_text(
                'Match history loading ...',
                parent=self.screen,
            )

        self.imgui.set_primary_window(window=self.screen, value=True)
        self.imgui.show_viewport()
        self.imgui.render_dearpygui_frame()

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
        self.imgui.delete_item(item='menu')
        self.imgui.add_menu_bar(tag='menu', parent=self.screen)

        # region Settings Menu
        self.imgui.add_menu_item(
            label='Settings',
            parent='menu',
            callback=lambda: (
                self.imgui.show_item(item='settings-popup'),
                self.center_window('settings-popup'),
            ),
        )
        # endregion Settings Menu

        # region Data Menu
        self.imgui.add_menu(label='Data', parent='menu', tag='menu-data')
        self.imgui.add_menu_item(
            label='Reload all data',
            parent='menu-data',
            callback=lambda: hinter.background.dataloader.data_loader.load_all(refresh=True)
        )
        # endregion Data Menu

        # region User Menu
        self.imgui.add_menu(label='User', parent='menu', tag='menu-user')

        # Option to add a user
        self.imgui.add_menu_item(
            label='Add User',
            parent='menu-user',
            callback=lambda: (hinter.users.add_user(self)),
        )
        self.add_menu_separator(parent='menu-user')

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
                label=username,
                parent='menu-user',
                callback=lambda: (hinter.users.select_user(self)),
                shortcut=selected,
            )

        # Option to remove a user
        if len(users) > 0:
            self.add_menu_separator(parent='menu-user', check=False)
            self.imgui.add_menu_item(
                label='Remove User',
                parent='menu-user',
                callback=lambda: (hinter.users.remove_user(self)),
            )
        # endregion User Menu

        # region Help Menu
        self.imgui.add_menu(label='Help', parent='menu', tag='menu-help')

        self.imgui.add_menu_item(
            label='Quick Guide',
            parent='menu-help',
            callback=lambda: (),
        )

        self.add_menu_separator(parent='menu-help', check=False)

        self.imgui.add_menu_item(
            label='Offer Feedback',
            parent='menu-help',
            callback=lambda: (),
        )

        self.imgui.add_menu_item(
            label='Report an Issue',
            parent='menu-help',
            callback=lambda: (),
        )

        self.imgui.add_menu_item(
            label='Suggest a feature',
            parent='menu-help',
            callback=lambda: (),
        )

        self.add_menu_separator(parent='menu-help', check=False)

        self.imgui.add_menu_item(
            label='Contribute Code',
            parent='menu-help',
            callback=lambda: (),
        )
        # endregion About Menu

        # region About Menu
        self.imgui.add_menu(label='About', parent='menu', tag='menu-about')

        self.imgui.add_menu_item(
            label='''Made by zbee, mostly in season 13
Copyright 2020 Ethan Henderson
Available under the GPLv3 license
Open Source at github.com/zbee/mobahinted''',
            parent='menu-about',
            enabled=False,
        )
        # endregion About Menu

    def add_menu_separator(self, parent: str, check: bool = None):
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
            print('hinter.UI: Cannot load image with un-handled type')
            # TODO: return a filler image
            return

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


UI = UI()
