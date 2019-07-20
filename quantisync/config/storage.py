import os
from pathlib import Path

APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Quantifico'
SETTINGS_PATH = APPDATA_PATH / 'settings.json'
CLOUD_SNAPSHOT_PATH = APPDATA_PATH / 'cloud_snapshot.dat'
LOG_PATH = APPDATA_PATH / 'sync_log.txt'
