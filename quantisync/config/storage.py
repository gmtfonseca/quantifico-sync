import os
from pathlib import Path

APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Quantifico'
OPTIONS_PATH = APPDATA_PATH / 'options.json'
CLOUD_SNAPSHOT_PATH = APPDATA_PATH / 'cloud_snapshot.dat'
LOG_PATH = APPDATA_PATH / 'sync_log.txt'
