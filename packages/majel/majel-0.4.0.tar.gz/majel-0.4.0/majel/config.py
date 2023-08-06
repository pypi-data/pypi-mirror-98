from pathlib import Path

import yaml

from .logger import Loggable


class ConfigurationError(Exception):
    pass


class Config(Loggable):
    """
    Python doesn't appear to have a simple parser for standard config files.
    ConfigParser will do .ini files, but if you just want a file with key/value
    pairs (as is pretty common in Unixland) there doesn't appear to be a way to
    do it outside of using a 3rd party module like dotenv. So, if you have to
    use an external library to do config, why not YAML?
    """

    CONFIG = Path("/etc/majel.yml")

    def __init__(self):

        self.mycroft_endpoint = None
        self.firefox_profile = None
        self.firefox_full_screen = True
        self.kodi_endpoint = None
        self.kodi_mount = None

        self.__update_from_config_file()

    def __update_from_config_file(self):

        if not self.CONFIG.exists():
            self.logger.warning(
                "No configuration file found at %s.  Proceeding with the "
                "defaults.",
                self.CONFIG,
            )
            return

        with self.CONFIG.open() as f:
            data = yaml.safe_load(f)

        for attribute in self.__dict__:
            if attribute not in data:
                continue
            setattr(self, attribute, data[attribute])


config = Config()
