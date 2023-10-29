#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import hinter

__all__ = ['show_info_popup']


def show_info_popup(title: str, text: str, width: int = 225, height: int = 125):
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
    hinter.UI.center_window('info-popup', [width, height])
