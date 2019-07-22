import os
from pathlib import Path

APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Quantifico'
SETTINGS_PATH = APPDATA_PATH / 'settings.json'
CLOUD_FOLDER_PATH = APPDATA_PATH / 'cloud.dat'
INVALID_FOLDER_PATH = APPDATA_PATH / 'invalid.dat'
LOG_PATH = APPDATA_PATH / 'sync_log.txt'
