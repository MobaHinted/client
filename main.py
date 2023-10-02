import hinter.ui.main as ui
import hinter.matchhistory
import hinter.settings

UI = ui.UI

match_history = hinter.matchhistory.MatchHistory()
match_history.show_match_screen()

hinter.settings.ready_settings_window()

UI.imgui.start_dearpygui()
UI.imgui.destroy_context()
