import os

from kal.utils.config import Config
from kal import path
from kal.utils.storage import Storage


def init():
    if not path.KAL_HOME_DIR.exists():
        os.makedirs(path.KAL_HOME_DIR)
    Config.initialize()
    Storage.initialize()
