import wx
import os

from ui.task_bar import MainTaskBarIcon
from ui.thread import BackgroundThread
from ui.events import EVT_UI
from quantisync.lib.factory import NfsFactory

# from ui.options import OptionsDialog

NF_PATH = os.path.abspath('../nf')
PICKLE_PATH = os.path.abspath('../quantisync.dat')
DELAY = 1.0


class MainFrame(wx.Frame):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.Bind(EVT_UI, self.onUpdateUI)
        self.taskBarIcon = MainTaskBarIcon(self)

        self.backgroundThread = self._criaBackgroundThread()
        self.backgroundThread.start()

    def _criaBackgroundThread(self):
        nfsObservador = NfsFactory.getObservador(NF_PATH, PICKLE_PATH)
        nfsHandler = NfsFactory.getHandler()
        return BackgroundThread(nfsObservador, nfsHandler, DELAY, self)

    def onUpdateUI(self, evt):
        if evt.isFatal():
            self.backgroundThread.abortar()

        self.taskBarIcon.updateUI(evt.getEstado())
