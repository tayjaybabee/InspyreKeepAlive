"""

File: inspyre_keep_alive/core/config/__init__.py
Project: InspyreKeepAlive
Description: 

Created: 2/14/23 - 21:49:34

"""
from configparser import ConfigParser
from pathlib import Path
from inspyre_keep_alive.__about__ import DEFAULT_CONF_DIR


class Config(ConfigParser):
    __default = {
            'DEFAULT': {
                'press_key': 'ctrl',
                'stop_key_combo': 'ctrl+shift+q',
                'press_interval': 30
            }
    }
    __auto_create = False
    __auto_load = False
    __auto_save = False
    __config_filepath = None
    __config_file_name = 'config.ini'
    __default_config_file_path = Path(DEFAULT_CONF_DIR).joinpath(__config_file_name)
    __skip_file_check = False

    def __init__(
            self,
            config_file_path=__default_config_file_path,
            skip_file_check=__skip_file_check,
            auto_create=False,
            auto_load = __auto_load,
            auto_save=__auto_save,
    ):
        self.auto_create = auto_create
        self.auto_save = auto_save
        self.auto_load = auto_load
        self.skip_file_check = skip_file_check
        self.config_file_path = Path(config_file_path)

        if self.auto_load and self.config_file_exists:
            self.load_config()
        elif not self.config_file_exists:
            if self.auto_create:
                self.create_config()



    @property
    def auto_create(self) -> bool:
        """

        Indicates whether the config file should be created automatically

        """
        return self.auto_create

    @auto_create.setter
    def auto_create(self, new):
        if not isinstance(new, bool):
            raise TypeError("auto_create must be a boolean")
        self.__auto_create = new

    @property
    def auto_load(self) -> bool:
        return self.__auto_load

    @auto_load.setter
    def auto_load(self, new: bool):
        if not isinstance(new, bool):
            raise TypeError('auto_load must be a boolean.')

        self.__auto_load = new

    @property
    def auto_save(self):
        return self.__auto_save

    @auto_save.setter
    def auto_save(self, new):
        if not isinstance(new, bool):
            raise TypeError('auto_save must be a boolean.')

        self.__auto_save = new

    @property
    def config_file_path(self) -> Path:
        """
        The set path for the config file to be saved to and loaded from.

        Returns:
            Path: The path to the config file.
        """
        return self.__config_file_path

    @config_file_path.setter
    def config_file_path(self, new: (Path, str)):
        if not isinstance(new, (Path, str)):
            raise TypeError("config_file_path must be a Path or a string.")
        if not str(new).endswith('.ini'):
            raise ValueError("config_file_path must be a file with a .ini extension.")
        new = Path(new).expanduser().absolute()

        self.__config_file_path = new

        if self.auto_load:
            self.load_config()

    @property
    def config_file_exists(self) -> bool:
        return self.__config_file_path.exists()

    @property
    def default_config(self):
        return self.__default

    @property
    def default_config_file_path(self):
        return self.__default_config_file_path

    @property
    def skip_file_check(self) -> bool:
        """

        Indicates whether we skip the config file-check on instantiation.

        """
        return self.__skip_file_check

    @skip_file_check.setter
    def skip_file_check(self, new):
        if not isinstance(new, bool):
            raise TypeError("skip_file_check must be a boolean.")

        self.__skip_file_check = new

    def create_config(self):
        if not self.config_file_path.exists():
            if not self.config_file_path == self.default_config_file_path:
                pass

    def load_config(self):
        """
        If there is a configuration file in the location indicated by :property:`config_file_path,
        we load it. Otherwise, an exception will be raised.

        """
        try:
            self.read(self.config_file_path)
        except FileNotFoundError as e:
            raise e from e
