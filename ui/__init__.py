import wx

from ui import main


def run():

    app = wx.App()
    main.start()
    app.MainLoop()
