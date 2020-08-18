import os.path
from dotenv import load_dotenv
from riotwatcher import LolWatcher
import json
import threading
import tkinter

import hinter.settings
import hinter.ui.progress

load_dotenv('.env')

watcher = LolWatcher(os.getenv('riotKey'))


class DataLoader:
    current_patch = ''
    data_path = './data/game_constants/'
    sub_data_paths = [
        'champions',
        'items',
        'maps',
        'masteries',
        'icons',
        'runes',
        'spells'
    ]
    data_loaded = {
        'champions': True,
        'items': True,
        'maps': True,
        'masteries': True,
        'icons': True,
        'runes': True,
        'spells': True
    }

    def __init__(self):
        self.current_patch = watcher.data_dragon.versions_for_region(hinter.settings.settings.region)['v']
        self.check_loaded()

    def check_loaded(self):
        # Verify data directory exists
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)

        for data in self.sub_data_paths:
            # Ensure data sub directories exist
            if not os.path.exists(self.data_path + data):
                os.mkdir(self.data_path + data)
                self.data_loaded[data] = False  # Mark as not having been loaded
            # Ensure data files exist
            if not os.path.exists(self.data_path + data + '.json'):
                open(self.data_path + data + '.json', 'w+')
                self.data_loaded[data] = False  # Mark as not having been loaded

        # TODO: Check files exist in directory, and that files are non-empty

        return self.data_loaded

    def load_all(self, root: tkinter.Tk, refresh=False):
        progress_popup = hinter.ui.progress.Progress(0, 'Downloading and processing: Champions')
        the_thread = threading.Thread(
            target=self.load_champions,
            args=(refresh,)
        )
        the_thread.start()
        the_thread.join()
        progress_popup.update(20, 'next')
        #self.load_items(refresh)
        #self.load_maps(refresh)
        #self.load_masteries(refresh)
        #self.load_icons(refresh)
        #self.load_runes(refresh)
        #self.load_spells(refresh)

        return self.check_loaded()

    def load_champions(self, refresh=False):
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

        with open(self.data_path + 'champions.json', 'w') as champion_file:
            json.dump(champions, champion_file)

        return self.check_loaded()

    def load_items(self, refresh=False):
        if self.data_loaded['items'] and not refresh:
            return False

        return self.check_loaded()

    def load_maps(self, refresh=False):
        if self.data_loaded['maps'] and not refresh:
            return False

        return self.check_loaded()

    def load_masteries(self, refresh=False):
        if self.data_loaded['masteries'] and not refresh:
            return False

        return self.check_loaded()

    def load_icons(self, refresh=False):
        if self.data_loaded['icons'] and not refresh:
            return False

        return self.check_loaded()

    def load_runes(self, refresh=False):
        if self.data_loaded['runes'] and not refresh:
            return False

        return self.check_loaded()

    def load_spells(self, refresh=False):
        if self.data_loaded['spells'] and not refresh:
            return False

        return self.check_loaded()


data_loader = DataLoader()
