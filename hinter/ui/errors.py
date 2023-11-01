#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import sys
import traceback
import urllib.parse
import webbrowser
from typing import Union

import cassiopeia
import hinter


class Errors:
    times_clicked: int

    _split_frame: bool
    _error_display: list[Union[str, dict]]
    _padding_height: int

    _error: Exception
    _python_version: str
    _trace: str = traceback.format_exc()

    def __init__(self):
        self._python_version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'

    def handle_error(self, error: Exception, split_frame: bool = True):
        self.times_clicked = 0
        self._error_display = []

        self._split_frame = split_frame

        self._error = error
        self._trace = traceback.format_exc()

        hinter.UI.clear_screen()

        self._sort_error()
        self._show_error()

    def _sort_error(self):
        error_string = str(self._error)

        if '503' in error_string:
            self._handle_riot_unavailable()
        elif '403' in error_string:
            self._handle_invalid_api_key()
        elif 'Max retries exceeded' in error_string:
            if 'getaddrinfo failed' in error_string:
                self._handle_no_internet()
            else:
                self._handle_proxy_down()
                if hinter.settings.pipeline_defaulted:
                    self._add_defaulted_pipeline_warning()
        else:
            self._handle_unspecified()

    def handle_clicks(self):
        self.times_clicked += 1

        if hinter.imgui.is_item_visible('sneaky_tooltip') or self.times_clicked == 3:
            hinter.imgui.set_clipboard_text(self._trace)
            self.times_clicked = 0

    def _add_hidden_traceback(self):
        with hinter.imgui.theme() as button_theme:
            with hinter.imgui.theme_component(hinter.imgui.mvImageButton):
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_Button, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_ButtonActive, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_ButtonHovered, (0, 0, 0, 0))
                hinter.imgui.add_theme_color(hinter.imgui.mvThemeCol_BorderShadow, (0, 0, 0, 0))

        # Only copy if the traceback is being shown, or if they triple-click
        sneaky_button = hinter.imgui.add_image_button(
            hinter.UI.filler_image,
            width=350,
            height=self._padding_height,
            background_color=(0, 0, 0, 0),
            callback=self.handle_clicks
        )

        hinter.imgui.bind_item_theme(sneaky_button, button_theme)

        with hinter.imgui.tooltip(parent=sneaky_button, delay=3, tag='sneaky_tooltip'):
            hinter.imgui.add_text(f'Click to copy the traceback.\n\n{self._trace}')

    def _show_error(self):
        # Configure the viewport
        hinter.imgui.set_viewport_min_width(350)
        hinter.imgui.set_viewport_width(350)
        hinter.imgui.set_viewport_min_height(600)
        hinter.imgui.set_viewport_height(600)
        hinter.imgui.set_viewport_resizable(False)

        # Set up the window
        with hinter.imgui.window(tag='error'):
            # Add a hidden traceback
            self._add_hidden_traceback()

            # Loop through the error display, adding each element specified
            for line in self._error_display:
                # Handle button elements
                if isinstance(line, dict):
                    hinter.imgui.add_button(
                        label=line['text'],
                        callback=line['callback'],
                        width=-1
                    )
                # Handle text elements
                else:
                    hinter.imgui.add_text(f'{line:^40}')

        # Show the window
        hinter.imgui.set_primary_window('error', True)
        hinter.UI.render_frames(split=self._split_frame)
        if not hinter.imgui.is_dearpygui_running():
            hinter.imgui.start_dearpygui()

        # Exit
        hinter.UI.exit_callback()
        sys.exit()

    def _handle_no_internet(self):
        self._padding_height = 250
        self._error_display = [
            'No internet connection.',
            'Please try again later.',
        ]

    def _handle_proxy_down(self):
        self._padding_height = 250
        self._error_display = [
            'MobaHinted Proxy server is down.',
            'Please try again later.',
        ]

    def _add_defaulted_pipeline_warning(self):
        self._padding_height = 150
        self._error_display.append('')
        self._error_display.append('You are seeing this because')
        self._error_display.append('your .env file was not found and')
        self._error_display.append('your pipeline was reset to default.')
        self._error_display.append('')
        self._error_display.append(
            {
                'text': 'See Setup Documentation',
                'callback': lambda: webbrowser.open('https://github.com/zbee/mobahinted#setup'),
            }
        )

    def _handle_riot_unavailable(self):
        region = cassiopeia.Region(hinter.settings.region)
        platform = cassiopeia.Platform[region.name].value.lower()

        self._padding_height = 150
        self._error_display = [
            'Riot services are unavailable.',
            'Please try again later.',
            '',
            'You can check the LoL status page:',
            {
                'text': 'Open status.rito Page',
                'callback': lambda: webbrowser.open(f'https://status.riotgames.com/lol?region={platform}'),
            },
            '(rarely posted if issues are unexpected)'
        ]

    def _handle_invalid_api_key(self):
        self._padding_height = 175
        self._error_display = [
            'This API key is invalid or expired.',
            'Please enter a new one.',
            '',
            'You can get a new one here:',
            {
                'text': 'Open developer.rito Page',
                'callback': lambda: webbrowser.open('https://developer.riotgames.com'),
            },
        ]

    def _handle_unspecified(self):
        self._padding_height = 200
        self._error_display = [
            'An Unknown Error has occurred.',
            'Please report this and try again later.',
            '',
            {
                'text': 'Report this Error on GitHub',
                'callback': lambda: webbrowser.open(
                    f'https://github.com/zbee/mobahinted/issues/new?title=Unknown%20Error&body=' +
                    urllib.parse.quote(
                        '\n\n\n\nPLEASE:\n' +
                        '- Describe what you were doing when the error occurred here.\n' +
                        '- Be as detailed as possible.\n' +
                        '- Add a descriptive title based on the last thing you were trying to do.' +
                        '\n\n\n\n\n\n\n\n---\n\n\n\n\n\n\n\nThis was the error encountered (On Python `' +
                        f'{self._python_version}`):\n```\n{self._error}\n```' +
                        f'\n\n\n\nTraceback:\n```\n{self._trace}\n```'
                    )
                ),
            },
        ]
