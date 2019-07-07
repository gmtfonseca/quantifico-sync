
from .main_task_bar_icon import MainTaskBarIcon
from modules.lib.factory import NfsFactory
from modules.loop_thread import LoopThread
from .events.task_bar_icon import EVT_UI
import wx
import os

NF_PATH = os.path.abspath('../nf')
PICKLE_PATH = os.path.abspath('../quantisync.dat')
DELAY = 1.0


class MainFrame(wx.Frame):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.Bind(EVT_UI, self.onUpdateUI)
        self.taskBarIcon = MainTaskBarIcon(self)
        self.loopThread = self._criaLoopThread()
        self.loopThread.start()

    def _criaLoopThread(self):
        nfsObservador = NfsFactory.getObservador(NF_PATH, PICKLE_PATH)
        nfsHandler = NfsFactory.getHandler()
        return LoopThread(nfsObservador, nfsHandler, DELAY, self)

    def onUpdateUI(self, evt):
        print(evt.getValue())
        self.taskBarIcon.updateUI(evt.getValue())
