#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import hinter


class Progress:
    current_percentage: int = 0

    def __init__(self, percentage: int, title: str, current_status: str):
        # Make sure percentage is 1-100
        if not 0 <= percentage <= 100:
            print('hinter.ui.Progress: progress percentage not usable')
            return

        self.current_percentage = percentage

        width = 325
        height = 115

        # Show the popup
        with hinter.imgui.window(
                label=title,
                modal=True,
                tag='progress-popup',
                width=width,
                height=height,
                no_resize=True,
                no_move=True,
                no_collapse=True,
                on_close=self.close,
                pos=[
                    int(hinter.imgui.get_viewport_width() / 2 - width / 2),
                    int(hinter.imgui.get_viewport_height() / 2 - height / 2),
                ]
        ):
            hinter.imgui.add_text(tag='progress-status', default_value=current_status, wrap=width-20)

            hinter.imgui.add_spacer(tag='progress-spacer', height=10)

            hinter.imgui.add_progress_bar(
                tag='progress-bar',
                parent='progress-popup',
                default_value=self.current_percentage,
                width=-1,
            )

    def update(self, percentage: int, current_status: str):
        # Make sure percentage is 1-100
        if not 0 <= percentage <= 100:
            print('hinter.ui.Progress.update: progress percentage not usable')
            return

        self.current_percentage = percentage
        hinter.imgui.configure_item(item='progress-status', default_value=current_status)
        hinter.imgui.set_value('progress-bar', 1/100 * self.current_percentage)

    # Ensure the popup can close itself
    def close(self):
        hinter.imgui.delete_item(item='progress-popup')
        hinter.imgui.delete_item(item='progress-status')
        hinter.imgui.delete_item(item='progress-spacer')
        hinter.imgui.delete_item(item='progress-bar')
        hinter.imgui.delete_item(item='progress-spacer-2')
        hinter.imgui.delete_item(item='progress-info')
