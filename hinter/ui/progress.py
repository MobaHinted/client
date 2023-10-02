import dearpygui.dearpygui


class Progress:
    current_percentage: int = 0
    imgui: dearpygui.dearpygui = dearpygui.dearpygui

    def __init__(self, percentage: int, title: str, current_status: str):
        # Make sure percentage is 1-100
        if not 0 <= percentage <= 100:
            print('hinter.ui.Progress: progress percentage not usable')
            return

        self.current_percentage = percentage

        width = 325
        height = 115

        # Show the popup
        with self.imgui.window(
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
                    int(self.imgui.get_viewport_width() / 2 - width / 2),
                    int(self.imgui.get_viewport_height() / 2 - height / 2),
                ]
        ):
            self.imgui.add_text(tag='progress-status', default_value=current_status, wrap=width-20)

            self.imgui.add_spacer(tag='progress-spacer', height=10)

            self.imgui.add_progress_bar(
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
        self.imgui.configure_item(item='progress-status', default_value=current_status)
        self.imgui.set_value('progress-bar', 1/100 * self.current_percentage)

    # Ensure the popup can close itself
    def close(self):
        self.imgui.delete_item(item='progress-popup')
        self.imgui.delete_item(item='progress-status')
        self.imgui.delete_item(item='progress-spacer')
        self.imgui.delete_item(item='progress-bar')
        self.imgui.delete_item(item='progress-spacer-2')
        self.imgui.delete_item(item='progress-info')
