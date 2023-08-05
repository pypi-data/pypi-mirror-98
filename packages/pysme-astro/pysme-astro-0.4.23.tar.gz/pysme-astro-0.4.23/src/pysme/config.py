"""
Handle the Json configuration file
At the moment it is only used for the LargeFileStorage
"""
import logging
from os.path import expanduser
import json

logger = logging.getLogger(__name__)


def _requires_load(func):
    def func_new(self, *args, **kwargs):
        if self._cfg is None:
            self.load()
        return func(self, *args, **kwargs)

    return func_new


class Config:
    def __init__(self, fname="~/.sme/config.json"):
        self.filename = fname
        self._cfg = None

    @property
    def filename(self):
        return str(self._filename)

    @filename.setter
    def filename(self, value):
        self._filename = expanduser(value)

    @_requires_load
    def __getitem__(self, key):
        return self._cfg[key]

    @_requires_load
    def __setitem__(self, key, value):
        self._cfg[key] = value

    def load(self):
        with open(self._filename, "r") as f:
            self._cfg = json.load(f)
        return self._cfg

    @_requires_load
    def save(self):
        with open(self._filename, "w") as f:
            json.dump(self._cfg, f)
