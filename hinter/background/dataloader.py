import os
import time
import zipfile

import cassiopeia
import requests

import hinter
import hinter.ui.progress


class DataLoader:
    current_patch: str = ''
    url_ranked_emblems = 'http://static.developer.riotgames.com/docs/lol/ranked-emblems.zip'
    url_ranked_positions = 'http://static.developer.riotgames.com/docs/lol/ranked-positions.zip'
    refresh: bool = False

    def __init__(self):
        self.current_patch = cassiopeia.get_version(region=hinter.settings.region)
        print('CURRENT PATCH DATA: ' + self.current_patch)

        if not os.path.exists(hinter.data.constants.PATH_RANKED_EMBLEMS + 'emblem-platinum.png'):
            self.load_all()

    def load_all(self, refresh: bool = False, popup: bool = True):

        # Save refresh variable, so we don't have to pass it into every method
        self.refresh = refresh

        title = 'Loading all Data'
        if refresh:
            title = 'Refreshing all Data'
            cassiopeia.configuration.settings.clear_sinks()
            cassiopeia.configuration.settings.expire_sinks()

        if popup:
            # Open the download popup, start downloading data and updating the
            #  progress bar as we go
            progress_popup = hinter.ui.progress.Progress(
                0, title, 'Downloading and processing: Champions'
            )
        cassiopeia.get_champions(region=hinter.settings.region)

        if popup:
            progress_popup.update(70, 'Downloading and processing: Items')
        cassiopeia.get_items(region=hinter.settings.region)

        if popup:
            progress_popup.update(80, 'Downloading and processing: Maps')
        cassiopeia.get_maps(region=hinter.settings.region)

        if popup:
            progress_popup.update(81, 'Downloading and processing: Spells')
        cassiopeia.get_summoner_spells(region=hinter.settings.region)

        if popup:
            progress_popup.update(82, 'Downloading and processing: Runes')
        cassiopeia.get_runes(region=hinter.settings.region)

        if popup:
            progress_popup.update(85, 'Downloading and processing: Rank icons')
        self.load_rank_icons(refresh)

        # Inform user data refresh completed, wait, then close the popup
        if popup:
            progress_popup.update(100, 'Data loading complete!\nWindow will close')
            time.sleep(4)
            progress_popup.close()

        # Do not update again until this is called, refresh data loaded checks
        self.refresh = False

    def load_rank_icons(self, refresh: bool = False):
        # Verify that emblems are not present, or a refresh is requested
        if not os.path.exists(hinter.data.constants.PATH_RANKED_EMBLEMS + 'emblem-platinum.png') or refresh:
            # Download ranked emblems
            emblems = requests.get(self.url_ranked_emblems)
            open(hinter.data.constants.PATH_DATA + 'emblems.zip', 'wb').write(emblems.content)

            # Unzip ranked emblems
            with zipfile.ZipFile(hinter.data.constants.PATH_DATA + 'emblems.zip', 'r') as emblems_zip:
                emblems_zip.extractall(hinter.data.constants.PATH_DATA)

            # Remove zip of ranked emblems
            os.remove('./data/emblems.zip')

        # Verify that position icons are not present, or a refresh is requested
        if not os.path.exists(hinter.data.constants.PATH_RANKED_LANES + 'Position_Plat-Mid.png') or refresh:
            # Download position icons
            positions = requests.get(self.url_ranked_positions)
            open(hinter.data.constants.PATH_DATA + 'positions.zip', 'wb').write(positions.content)

            # Unzip position icons
            with zipfile.ZipFile(hinter.data.constants.PATH_DATA + 'positions.zip', 'r') as positions_zip:
                positions_zip.extractall(hinter.data.constants.PATH_RANKED_LANES)

            # Remove zip of position icons
            os.remove(hinter.data.constants.PATH_DATA + 'positions.zip')
