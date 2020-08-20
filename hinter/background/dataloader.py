import os
from typing import Dict
from dotenv import load_dotenv
from riotwatcher import LolWatcher
import json

import time

import hinter.settings
import hinter.ui.progress

load_dotenv('.env')

watcher = LolWatcher(os.getenv('riotKey'))


class DataLoader:
    current_patch = ''
    data_path = './data/game_constants/'
    data_loaded: Dict[str: bool] = {
        'champions': True,
        'items': True,
        'maps': True,
        'icons': True,
        'runes': True,
        'spells': True
    }
    data_needs = {
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
        }
    }

    def __init__(self):
        hinter.settings.settings.load_settings()
        self.current_patch = watcher.data_dragon.versions_for_region(hinter.settings.settings.region)['v']
        self.check_loaded()

    def check_loaded(self):
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

    def load_all(self, refresh=False):
        progress_popup = hinter.ui.progress.Progress(0, 'Downloading and processing: Champions')
        start_time = time.process_time()

        start_champ_time = time.process_time()
        self.load_champions(refresh)
        end_champ_time = time.process_time()
        champ_time = end_champ_time - start_champ_time
        print('champ time: ' + str(champ_time))

        start_items_time = time.process_time()
        progress_popup.update(20, 'Downloading and processing: Items')
        self.load_items(refresh)
        end_items_time = time.process_time()
        items_time = end_items_time - start_items_time
        print('items time: ' + str(items_time))

        start_maps_time = time.process_time()
        progress_popup.update(40, 'Downloading and processing: Maps')
        self.load_maps(refresh)
        end_maps_time = time.process_time()
        maps_time = end_maps_time - start_maps_time
        print('maps time: ' + str(maps_time))

        start_icons_time = time.process_time()
        progress_popup.update(60, 'Downloading and processing: Icons')
        self.load_icons(refresh)
        end_icons_time = time.process_time()
        icons_time = end_icons_time - start_icons_time
        print('icons time: ' + str(icons_time))

        # self.load_icons(refresh)
        # self.load_runes(refresh)
        # self.load_spells(refresh)

        end_time = time.process_time() - start_time
        print('total download time: ' + str(end_time))

        return self.check_loaded()

    def load_champions(self, refresh=False):
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['champions'] and not refresh:
            return False

        # Load champion data
        champions = watcher.data_dragon.champions(self.current_patch, full=True)

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
                spell['id'] = spell['id'][-1]
                spell['image'] = spell['image']['full']
            champion['passive']['image'] = champion['passive']['image']['full']

        # Save data to file
        with open(self.data_path + 'champions.json', 'w') as champions_file:
            json.dump(champions, champions_file)

        return self.check_loaded()

    def load_items(self, refresh=False):
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['items'] and not refresh:
            return False

        # Load item data
        items = watcher.data_dragon.items(self.current_patch)

        # Trim down data
        del items['basic']

        # Save item data
        with open(self.data_path + 'items.json', 'w') as items_file:
            json.dump(items, items_file)

        return self.check_loaded()

    def load_maps(self, refresh=False):
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['maps'] and not refresh:
            return False

        # Load maps data
        maps = watcher.data_dragon.maps(self.current_patch)

        # Trim data
        for trash, ind_map in maps['data'].items():
            ind_map['image'] = ind_map['image']['full']

        # Save maps data
        with open(self.data_path + 'items.json', 'w') as items_file:
            json.dump(maps, items_file)

        return self.check_loaded()

    def load_icons(self, refresh=False):
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['icons'] and not refresh:
            return False

        # Load icons data
        icons = watcher.data_dragon.profile_icons(self.current_patch)

        # Trim data
        for trash, icon in icons.items():
            icon['image'] = icon['image']['full']

        # Save icons data
        with open(self.data_path + 'icons.json', 'w') as items_file:
            json.dump(icons, items_file)

        return self.check_loaded()

    def load_runes(self, refresh=False):
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['runes'] and not refresh:
            return False

        return self.check_loaded()

    def load_spells(self, refresh=False):
        # Skip loading if data is already loaded and a refresh was not requested
        if self.data_loaded['spells'] and not refresh:
            return False

        return self.check_loaded()


data_loader = DataLoader()
