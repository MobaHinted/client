#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import os
import shutil
import time
import zipfile

import cassiopeia
import requests

import hinter


class DataLoader:
    current_patch: str = ''
    url_ranked_emblems = 'https://static.developer.riotgames.com/docs/lol/ranked-emblems-latest.zip'
    refresh: bool = False

    def __init__(self):
        self.current_patch = cassiopeia.get_version(region=hinter.settings.region)
        print('CURRENT PATCH DATA: ' + self.current_patch)

        if not os.path.exists(hinter.data.constants.PATH_RANKED_EMBLEMS + 'Rank=Emerald.png'):
            self.load_all()

    # noinspection PyUnboundLocalVariable
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
            progress_popup = hinter.Progress.Progress(
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
        if not os.path.exists(hinter.data.constants.PATH_RANKED_EMBLEMS + 'Rank=Emerald.png') or refresh:
            # Remove old ranked emblems if they're present
            if os.path.exists(hinter.data.constants.PATH_RANKED_EMBLEMS):
                shutil.rmtree(hinter.data.constants.PATH_RANKED_EMBLEMS)

            # Download ranked emblems
            emblems = requests.get(self.url_ranked_emblems)
            open(hinter.data.constants.PATH_DATA + 'emblems.zip', 'wb').write(emblems.content)

            # Unzip ranked emblems
            with zipfile.ZipFile(hinter.data.constants.PATH_DATA + 'emblems.zip', 'r') as emblems_zip:
                emblems_zip.extractall(hinter.data.constants.PATH_DATA)

            # Remove zip of ranked emblems
            os.remove(hinter.data.constants.PATH_DATA + 'emblems.zip')

            # Rename the folder in the zip
            shutil.move(
                hinter.data.constants.PATH_DATA + 'Ranked Emblems Latest',
                hinter.data.constants.PATH_RANKED_EMBLEMS
            )
