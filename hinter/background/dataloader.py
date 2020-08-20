import os
import time
import json
import requests
import tarfile
from retry import retry
from typing import Dict

import hinter.ui.progress


class DataLoader:
    current_patch: str = ''
    data_path = './data/game_constants/'
    temp_data_path = data_path + 'temp/'
    url_ranked_emblems = 'http://static.developer.riotgames.com/docs/lol/ranked-emblems.zip'
    url_ranked_positions = 'http://static.developer.riotgames.com/docs/lol/ranked-positions.zip'
    url_dragon_tail = ''
    data_loaded: Dict[str, bool] = {
        'champions': True,
        'items': True,
        'maps': True,
        'icons': True,
        'runes': True,
        'spells': True,
        'ranks': True
    }
    data_needs: Dict[str, Dict[str, bool]] = {
        'champions': {
            'images': True,
            'json': True
        },
        'items': {
            'images': True,
            'json': True
        },
        'maps': {
            'images': True,
            'json': True
        },
        'icons': {
            'images': True,
            'json': False
        },
        'runes': {
            'images': True,
            'json': True
        },
        'spells': {
            'images': True,
            'json': True
        },
        'ranks': {
            'images': True,
            'json': False
        }
    }
    refresh: bool = False

    def __init__(self):
        self.current_patch = hinter.watcher.data_dragon.versions_for_region(hinter.settings.region)['v']
        self.check_loaded()
        self.url_dragon_tail = 'https://ddragon.leagueoflegends.com/cdn/dragontail-' + self.current_patch + '.tgz'

    def check_loaded(self) -> Dict[str, bool]:
        # Verify data directory exists
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)

        for data, trash in self.data_loaded.items():
            # Check images subdirectory for data
            if self.data_needs[data]['images']:
                # Ensure data sub directories exist
                if not os.path.exists(self.data_path + data):
                    os.mkdir(self.data_path + data)
                    self.data_loaded[data] = False  # Mark as not loaded
                # TODO: Ensure images exist in data sub directories

            # Check JSON file for data
            if self.data_needs[data]['json']:
                # Ensure data files exist
                if not os.path.exists(self.data_path + data + '.json'):
                    open(self.data_path + data + '.json', 'w+')
                    self.data_loaded[data] = False  # Mark as not loaded
                # Ensure data files have content
                if os.stat(self.data_path + data + '.json').st_size == 0:
                    self.data_loaded[data] = False  # Mark as not loaded
        return self.data_loaded

    def load_all(self, refresh: bool = False) -> Dict[str, bool]:
        # Save refresh variable so we don't have to pass it into every method
        self.refresh = refresh

        # Open the download popup, start downloading data and updating the progress bar as we go
        progress_popup = hinter.ui.progress.Progress(0, 'Downloading and processing: Champions')
        self.load_champions()

        progress_popup.update(40, 'Downloading and processing: Items')
        self.load_items()

        progress_popup.update(45, 'Downloading and processing: Maps')
        self.load_maps()

        progress_popup.update(46, 'Downloading and processing: Runes')
        self.load_runes()

        progress_popup.update(49, 'Downloading and processing: Spells')
        self.load_spells()

        progress_popup.update(50, 'Downloading: Images')
        self.download_images()

        progress_popup.update(58, 'Processing: Images')
        self.process_images()

        progress_popup.update(90, 'Downloading and processing: Rank icons')
        # TODO: Implement rank icon downloading
        #  (http://static.developer.riotgames.com/docs/lol/ranked-emblems.zip for ranked emblems,
        #  http://static.developer.riotgames.com/docs/lol/ranked-positions.zip for ranked positions)
        #  self.load_rank_icons()

        # Inform user data refresh completed, wait, then close the popup
        progress_popup.update(100, 'Data refresh complete! Window will close ...')
        time.sleep(3)
        progress_popup.close()

        # Do not update again until this is called, refresh data loaded checks
        self.refresh = False
        # TODO: implement download cleanup | self.cleanup_downloads()
        return self.check_loaded()

    def load_champions(self) -> Dict[str, bool]:
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['champions'] and not self.refresh:
            return self.data_loaded

        # Load champion data
        champions = hinter.watcher.data_dragon.champions(self.current_patch, full=True)

        # Trim down data
        for trash, champion in champions['data'].items():
            # Remove unnecessary keys from list
            del champion['lore']
            del champion['blurb']
            del champion['skins']
            del champion['allytips']
            del champion['enemytips']
            del champion['partype']
            del champion['info']

            # Remove unnecessary builds
            remove = []
            for key in range(len(champion['recommended'])):
                build = champion['recommended'][key]
                if build['mode'] == 'INTRO':
                    remove.append(key)
            for key in remove:
                del champion['recommended'][key]

            # Reformat data
            champion['image'] = champion['image']['full']
            for spell in champion['spells']:
                spell['image'] = spell['image']['full']
            champion['passive']['image'] = champion['passive']['image']['full']

        # Save data to file
        with open(self.data_path + 'champions.json', 'w') as champions_file:
            json.dump(champions, champions_file)

        return self.check_loaded()

    def load_items(self) -> Dict[str, bool]:
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['items'] and not self.refresh:
            return self.data_loaded

        # Load item data
        items = hinter.watcher.data_dragon.items(self.current_patch)

        # Trim down data
        del items['basic']

        # Save item data
        with open(self.data_path + 'items.json', 'w') as items_file:
            json.dump(items, items_file)

        return self.check_loaded()

    def load_maps(self) -> Dict[str, bool]:
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['maps'] and not self.refresh:
            return self.data_loaded

        # Load maps data
        maps = hinter.watcher.data_dragon.maps(self.current_patch)

        # Trim data
        for trash, ind_map in maps['data'].items():
            ind_map['image'] = ind_map['image']['full']

        # Save maps data
        with open(self.data_path + 'maps.json', 'w') as maps_file:
            json.dump(maps, maps_file)

        return self.check_loaded()

    def load_runes(self) -> Dict[str, bool]:
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['runes'] and not self.refresh:
            return self.data_loaded

        # Load runes data
        runes = hinter.watcher.data_dragon.runes_reforged(self.current_patch)

        # Save runes data
        with open(self.data_path + 'runes.json', 'w') as runes_file:
            json.dump(runes, runes_file)

        return self.check_loaded()

    def load_spells(self) -> Dict[str, bool]:
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['spells'] and not self.refresh:
            return self.data_loaded

        # Load spells data
        spells = hinter.watcher.data_dragon.summoner_spells(self.current_patch)

        # Reformat data
        spells = {
            'type': 'summonerSpells',
            'version': self.current_patch,
            'data': spells
        }

        # Save spells data
        with open(self.data_path + 'spells.json', 'w') as spells_file:
            json.dump(spells, spells_file)

        return self.check_loaded()

    @retry(tries=3, delay=1)
    def download_images(self) -> bool:
        # Create temporary data directory
        file_path = self.temp_data_path + 'dragon_tail.tgz'
        if not os.path.exists(self.temp_data_path):
            os.mkdir(self.temp_data_path)
        elif os.stat(file_path).st_size > 0:
            return True

        # Download dragon tail data
        dragon_tail = requests.get(self.url_dragon_tail)
        open(file_path, 'wb').write(dragon_tail.content)
        file_size = os.stat(file_path).st_size

        # Verify download
        return True if file_size > 0 else False

    def process_images(self) -> None:
        file_path = self.temp_data_path + 'dragon_tail.tgz'

        # Extract images
        dragon_tail_tar = tarfile.open(file_path, 'r:gz')
        dragon_tail_tar.extractall(self.temp_data_path)
        dragon_tail_tar.close()

        """
        /<current-patch>/img/champion/<champion name>.png for load_champions
            /<current-patch>/img/spell/<spell name>.png for ability spell icons
            /<current-patch>/img/passive/<champion name>_P.png for passive spell icons
            /img/champions/splash/<champion name>_0.png for splash backgrounds
        /<current-patch>/img/item/<item id>.png for load_items
        /<current-patch>/img/map/<map id>.png for load_maps
        /<current-patch>/img/profileicon/<icon id>.png for load_icons
        /img/perk-images/Styles/ for load_runes, "icon" has full path needed
        /<current-patch>/img/spell/<spell name>.png for load_spells
        """


data_loader = DataLoader()
