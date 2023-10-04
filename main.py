import hinter.ui.main as ui
import hinter.matchhistory


def continue_drawing(ui, render):
    match_history = hinter.matchhistory.MatchHistory(ui)
    match_history.show_match_screen(render)


UI = ui.UI(continue_drawing)

UI.imgui.start_dearpygui()
UI.imgui.destroy_context()
