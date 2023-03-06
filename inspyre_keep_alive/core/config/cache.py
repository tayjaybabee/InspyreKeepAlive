"""

File: inspyre_keep_alive/core/config/cache.py
Project: InspyreKeepAlive
Description: 

Created: 2/15/23 - 15:32:32

"""

import os
import time
import dill
import appdirs
from pathlib import Path

from inspyre_keep_alive.__about__ import __PROG__ as PROG_NAME, __AUTHOR__ as AUTHOR
from inspyre_keep_alive.core import ISL


LOG_NAME = f'{PROG_NAME}.core.cache'


log = ISL.device.add_child(LOG_NAME)
log.debug(f'{LOG_NAME} loaded.')


class ConfCache:
    """A class representing a dictionary with automatic saving and loading to a file.

    Attributes:

        auto_save (bool, optional):
            Whether to automatically save an already created cache file. (Default: True)

        auto_create (bool, optional):
            Whether to automatically create the dictionary and save it to file if it does not exist. Default is True.

        auto_load (bool, optional):
            Whether to automatically load the dictionary from file if it exists. Default is True.

    Properties:

        contents (dict):
            The dictionary containing the contents of the ConfCache object.

        filepath (str):
            The file path where the dictionary is saved.

        created (str):
            The creation date of the dictionary as a string in the format "YYYY-MM-DD HH:MM:SS".

        age (str):
            The age of the dictionary as a string in the format "DDD:HH:MM:SS".

        auto_save (bool):
            Whether auto_save is enabled or not.

    Methods:
        save():
            Saves the dictionary to file.

        load():
            Loads the dictionary from file.

        update_last_start():
            Updates the "Last start" field of the dictionary with the current time and saves the dictionary to file
            (if auto_save is enabled).

    Raises:
        ValueError: If auto_save property is set to a non-boolean value.
    """
    def __init__(self,
                 auto_create: bool = True,
                 auto_load: bool = True,
                 auto_save: bool = True
                 ):
        self.LOG_NAME = f'{LOG_NAME}.ConfCache'
        self.LOG = ISL.device.add_child(self.LOG_NAME)

        self.LOG.debug('Initializing...')

        self._contents = { }
        self.auto_save = auto_save
        self.auto_create = auto_create
        self.auto_load = auto_load

        self.LOG.debug(
            f'Starting values:\n'
            f'contents: {self.contents or "None"}\n'
            f'auto_save: {self.auto_save}\n'
            f'auto_create: {self.auto_create}\n'
            f'auto_load: {self.auto_load}'
        )

        if os.path.isfile(self.filepath):
            if self.auto_load:
                self.load()
        elif self.auto_create:
            self.update_last_start()
            self.save()

    @property
    def contents(self):
        return self._contents

    @property
    def filepath(self):
        return os.path.join(
            appdirs.user_cache_dir(
                appname=PROG_NAME,
                appauthor=AUTHOR
            ),
            'mydict.pkl'
        )

    @property
    def created(self):
        return self._contents.get('Creation date')

    @property
    def age(self):
        if self.created is None:
            return ''
        created_time = time.strptime(self.created, '%Y-%m-%d %H:%M:%S')
        elapsed_time = time.time() - time.mktime(created_time)
        days = elapsed_time // (24 * 60 * 60)
        elapsed_time -= days * 24 * 60 * 60
        hours = elapsed_time // (60 * 60)
        elapsed_time -= hours * 60 * 60
        minutes = elapsed_time // 60
        seconds = elapsed_time - minutes * 60
        return f'{int(days):03}:{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

    @property
    def auto_save(self):
        return self._auto_save

    @auto_save.setter
    def auto_save(self, value):
        if isinstance(value, bool):
            self._auto_save = value
        else:
            raise ValueError("Autosave property can only be set to a boolean value.")

    def save(self):

        fp = Path(self.filepath).parent

        if not fp.exists():
            fp.mkdir()


        with open(self.filepath, 'wb') as f:
            dill.dump(self._contents, f)

    def load(self):
        try:
            with open(self.filepath, 'rb') as f:
                self._contents = dill.load(f)
        except FileNotFoundError:
            print(f"Cannot find file {self.filepath}")
            if self.auto_create:
                self.update_last_start()
                self.save()

    def update_last_start(self):
        self._contents['Last start'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if self.created is None:
            self._contents['Creation date'] = self._contents['Last start']
        if self._auto_save:
            self.save()
