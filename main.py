#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

# region Show access violations
try:
    import faulthandler
    if __name__ == "__main__":
        faulthandler.enable()
except RuntimeError:
    pass
# endregion Show access violations

import hinter
# noinspection PyPep8Naming
import hinter.match_history.history_data as History


def continue_drawing(render):
    History.HistoryData(render)


hinter.UI = hinter.UIFunctionality(continue_drawing)

hinter.UI.imgui.start_dearpygui()
hinter.UI.imgui.destroy_context()
