#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

# region Show access violations
try:
    import faulthandler
    if __name__ == "__main__":
        faulthandler.enable()
except RuntimeError:
    pass
# TODO: Catch these errors `Windows Fatal Error: access violation (0xc0000005)`:
#   https://stackoverflow.com/a/74601939/1843510
#   probably in `launcher.py`. Just relaunch the application if one occurs, and log it.
#     They're intermittently coming from `dpg.add_image` and can be ignored
# endregion Show access violations

import hinter
# noinspection PyPep8Naming
import hinter.match_history.history_data as History

# Make sure all files and folders exist
hinter.data.management.Setup()


def continue_drawing():
    History.HistoryData()


hinter.UI = hinter.UIFunctionality(continue_drawing)

hinter.UI.imgui.start_dearpygui()
hinter.UI.imgui.destroy_context()
