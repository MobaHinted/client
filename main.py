import hinter.ui.main as ui
# noinspection PyPep8Naming
import hinter.match_history.match_data as MatchData


def continue_drawing(ui, render):
    MatchData.MatchData(ui, render)


UI = ui.UI(continue_drawing)

UI.imgui.start_dearpygui()
UI.imgui.destroy_context()
