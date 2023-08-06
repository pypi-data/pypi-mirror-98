import os
from pathlib import Path


SOURCE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = SOURCE_DIR.parent
USER_HOME_DIR = Path(os.getenv('HOME'))

if os.getenv('DROPBOX_PATH'):
    DROPBOX_DIR = Path(os.getenv('DROPBOX_PATH'))
else:
    DROPBOX_DIR = USER_HOME_DIR / 'Dropbox'

if os.getenv('KAL_HOME'):
    KAL_HOME_DIR = Path(os.getenv('KAL_HOME'))
else:
    KAL_HOME_DIR = USER_HOME_DIR / '.kal'

CONFIG_FILE = KAL_HOME_DIR / 'config.json'
STORAGE_FILE = KAL_HOME_DIR / 'storage.json'
