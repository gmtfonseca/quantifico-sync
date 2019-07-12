import logging

import wx

from ui.main import MainFrame


def run():
    logging.basicConfig(level=logging.DEBUG)

    app = wx.App()

    MainFrame(None)
    app.MainLoop()
