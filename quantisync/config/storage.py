import os
from pathlib import Path

APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Quantifico'
SYNC_DATA_PATH = APPDATA_PATH / 'sync_data.json'
CLOUD_FOLDER_PATH = APPDATA_PATH / 'cloud.dat'
BLACKLISTED_FOLDER_PATH = APPDATA_PATH / 'blacklisted.dat'
LOG_PATH = APPDATA_PATH / 'sync_log.txt'
DB_PATH = APPDATA_PATH / 'quantisync.db'
DB_TEST_PATH = Path('tests/fixture/quantisync_test.db')
