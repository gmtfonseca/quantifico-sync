import os
from pathlib import Path

APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Quantifico'
SETTINGS_PATH = APPDATA_PATH / 'settings.json'
CLOUD_FOLDER_PATH = APPDATA_PATH / 'cloud.dat'
BLACKLISTED_FOLDER_PATH = APPDATA_PATH / 'blacklisted.dat'
LOG_PATH = APPDATA_PATH / 'sync_log.txt'
