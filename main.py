import hinter
# noinspection PyPep8Naming
import hinter.match_history.match_data as MatchData


def continue_drawing(ui, render):
    hinter.UIMenus(ui).add_menu()
    MatchData.MatchData(ui, render)


UI = hinter.UIFunctionality(continue_drawing)

UI.imgui.start_dearpygui()
UI.imgui.destroy_context()
