import os
import webbrowser
from typing import Union

import PIL.Image as Image
import cassiopeia
import numpy as np
import requests

import hinter


class UIFunctionality(hinter.ui.UI):
    font: dict = {}
    filler_image: str
    _filler: str = ''
    imgui = hinter.imgui  # TODO: Remove this, import hinter.user and match history to __init__ and include that in main

    def __init__(self, move_on_callback):
        super().__init__(move_on_callback)

    def new_screen(self, tag: str, set_primary: bool = False):
        # Set the new window as the primary window when ready
        if set_primary:
            hinter.imgui.set_primary_window(window=tag, value=True)
            return

        if hinter.imgui.does_item_exist(tag):
            # Empty the old window
            self.clear_screen()

        # Add a new window
        hinter.imgui.add_window(tag=tag)

        # Save the new window tag
        self.screen = tag

        # Add the menu bar back
        self.render_frames()
        hinter.Menu.add_menu()

    def clear_screen(self):
        hinter.imgui.delete_item(item=self.screen)

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

    @property
    def filler_image(self):
        if not hinter.imgui.does_alias_exist('CACHED_IMAGE-filler'):
            self._filler = self.load_image(
                'filler',
                hinter.data.constants.IMAGE_TYPE_FILE,
                f'{hinter.data.constants.PATH_ASSETS}filler.png',
                size=(1, 1)
            )
        return self._filler

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
