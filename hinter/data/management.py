#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import os
import time
import zipfile

import requests

import hinter.data.constants as constants


def file_empty(file: str):
    return os.stat(file).st_size == 0


# noinspection PyMethodMayBeStatic
class Setup:
    _folders = [
        constants.PATH_DATA,
        constants.PATH_CASSIOPEIA,
        constants.PATH_IMAGES,
        constants.PATH_RANKED_EMBLEMS,
    ]
    _files = [
        constants.PATH_SETTINGS_FILE,
        constants.PATH_CHAMPION_ROLE_DATA_FILE,
        constants.PATH_USERS_FILE,
        constants.PATH_IMGUI_FILE,
        constants.PATH_FRIENDS_FILE,
    ]
    _assets_url = 'https://codeload.github.com/zbee/mobahinted/zip/refs/heads/master'

    def __init__(self):
        self.setup_directories()
        self.setup_files()
        self.ensure_assets()

    def _make_empty_folder_if_does_not_exist(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def setup_directories(self):
        for folder in self._folders:
            self._make_empty_folder_if_does_not_exist(folder)

    def _make_empty_file_if_does_not_exist(self, path):
        if not os.path.exists(path):
            file = open(path, 'w+')
            file.close()

    def setup_files(self):
        for file in self._files:
            self._make_empty_file_if_does_not_exist(file)

    def ensure_assets(self):
        if os.path.exists(constants.PATH_ASSETS):
            return

        # Name for zip file
        zip_file = 'repository.zip'
        # Make assets folder
        os.mkdir(constants.PATH_ASSETS)

        # Download assets
        fresh_assets = requests.get(self._assets_url)
        # Save assets
        open(constants.PATH_ASSETS + zip_file, 'wb').write(fresh_assets.content)

        archive = zipfile.ZipFile(constants.PATH_ASSETS + zip_file, 'r')
        infos = archive.infolist()

        # Iterate over the zip's files
        for info in infos:
            # Save assets into the assets folder
            if 'assets/' in info.filename:
                info.filename = info.filename.split('/')[-1]
                # Skip the assets folder itself, only getting its contents
                if info.filename != '':
                    archive.extract(info, constants.PATH_ASSETS)

        archive.close()

        # Remove zip file
        os.remove(constants.PATH_ASSETS + zip_file)


# noinspection PyMethodMayBeStatic
class Clean:

    # TODO: Is a method needed to clean up cass/image data?

    def is_file_older_than_x_days(self, file, days: int = 1, by_access_time: bool = False):
        # Get the file's last modified time
        file_time = os.path.getmtime(file)
        # Or last access time
        if by_access_time:
            file_time = os.path.getatime(file)

        # Check against 24 hours * days
        return (time.time() - file_time) / 3600 > 24 * days
