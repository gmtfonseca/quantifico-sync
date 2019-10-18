import os
from pathlib import Path

import wx

from ui import main
from quantisync.core.app import App


APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Quantifico'

config = {
    'storage': {
        'SYNC_DATA_PATH': APPDATA_PATH / 'sync_data.json',
        'CLOUD_SNAPSHOT_PATH': APPDATA_PATH / 'cloud.dat',
        'BLACKLISTED_SNAPSHOT_PATH': APPDATA_PATH / 'blacklisted.dat'
    },
    'auth': {
        'SERVICE_NAME': 'quantisync',

    },
    'network': {
        'HTTP_URL': 'http://localhost:4000/',
        'MAX_BATCH_SIZE': {
            'STREAM': 40,
            'DELETE': 100
        }
    },
    'sync': {
        'NF_EXTENSION': 'XML',
        'DELAY': 2,
    }
}


def run():
    wxApp = wx.App()

    app = App(config)
    main.start(app)

    wxApp.MainLoop()
