import os
from pathlib import Path

APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Quantifico'
SETTINGS_PATH = APPDATA_PATH / 'settings.json'
SERVER_SNAPSHOT_PATH = APPDATA_PATH / 'server_snapshot.dat'
INVALID_SNAPSHOT_PATH = APPDATA_PATH / 'invalid_snapshot.dat'
LOG_PATH = APPDATA_PATH / 'sync_log.txt'
