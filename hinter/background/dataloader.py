import time
import requests
from retry import retry

import hinter.ui.progress
import cassiopeia


class DataLoader:
    current_patch: str = ''
    url_ranked_emblems = 'http://static.developer.riotgames.com/docs/lol/ranked-emblems.zip'
    url_ranked_positions = 'http://static.developer.riotgames.com/docs/lol/ranked-positions.zip'
    refresh: bool = False

    def __init__(self):
        self.current_patch = cassiopeia.get_version()

    def load_all(self, refresh: bool = False):
        # Save refresh variable so we don't have to pass it into every method
        self.refresh = refresh

        if refresh:
            cassiopeia.configuration.settings.clear_sinks()
            cassiopeia.configuration.settings.expire_sinks()

        # Open the download popup, start downloading data and updating the
        #  progress bar as we go
        progress_popup = hinter.ui.progress.Progress(
            0, 'Downloading and processing: Champions'
        )
        cassiopeia.get_champions()

        progress_popup.update(70, 'Downloading and processing: Items')
        cassiopeia.get_items()

        progress_popup.update(80, 'Downloading and processing: Maps')
        cassiopeia.get_maps()

        progress_popup.update(81, 'Downloading and processing: Spells')
        cassiopeia.get_summoner_spells()

        progress_popup.update(82, 'Downloading and processing: Runes')
        cassiopeia.get_runes()

        progress_popup.update(85, 'Downloading and processing: Rank icons')
        # TODO: Implement rank icon downloading
        #  (http://static.developer.riotgames.com/docs/lol/ranked-emblems.zip for ranked emblems,
        #  http://static.developer.riotgames.com/docs/lol/ranked-positions.zip for ranked positions)
        #  self.load_rank_icons()

        # Inform user data refresh completed, wait, then close the popup
        progress_popup.update(100, 'Data refresh complete! Window will close')
        time.sleep(3)
        progress_popup.close()

        # Do not update again until this is called, refresh data loaded checks
        self.refresh = False


data_loader = DataLoader()
