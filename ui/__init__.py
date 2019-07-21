import logging

import wx

from ui import main


def run():
    logging.basicConfig(level=logging.DEBUG)

    app = wx.App()
    main.start()
    app.MainLoop()
