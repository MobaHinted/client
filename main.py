import hinter
# noinspection PyPep8Naming
import hinter.match_history.match_data as MatchData


def continue_drawing(ui, render):
    hinter.Menu = hinter.UIMenus(ui)
    hinter.UI = ui
    MatchData.MatchData(ui, render)


hinter.UI = hinter.UIFunctionality(continue_drawing)

hinter.UI.imgui.start_dearpygui()
hinter.UI.imgui.destroy_context()
