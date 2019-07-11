from quantisync.ui.main_frame import MainFrame
import wx
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = wx.App()
    MainFrame(None)
    app.MainLoop()


if __name__ == "__main__":
    main()
