import wx

from ui import main
from ui.app import app


def run():
    wxApp = wx.App()
    main.start(app)
    wxApp.MainLoop()
