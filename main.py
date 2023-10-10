import hinter
# noinspection PyPep8Naming
import hinter.match_history.match_data as MatchData


def continue_drawing(ui, render):
    MatchData.MatchData(ui, render)


UI = hinter.UIFunctionality(continue_drawing)

UI.imgui.start_dearpygui()
UI.imgui.destroy_context()
