#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import hinter
# noinspection PyPep8Naming
import hinter.match_history.history_data as History


def continue_drawing(ui, render):
    hinter.Menu = hinter.UIMenus(ui)
    hinter.UI = ui
    History.HistoryData(ui, render)


hinter.UI = hinter.UIFunctionality(continue_drawing)

hinter.UI.imgui.start_dearpygui()
hinter.UI.imgui.destroy_context()
