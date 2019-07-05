
from .main_task_bar_icon import MainTaskBarIcon
from modules.lib.factory import ObservadorFactory
from modules.loop_thread import LoopThread
import wx
import os

NF_PATH = os.path.abspath('../nf')
PICKLE_PATH = os.path.abspath('../quantisync.dat')
DELAY = 5.0


class MainFrame(wx.Frame):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.taskBarIcon = MainTaskBarIcon(self)
        self.loopThread = self._criaLoopThread()
        self.loopThread.start()

    def _criaLoopThread(self):
        observador = ObservadorFactory.getObservadorNfs(NF_PATH, PICKLE_PATH)
        return LoopThread(observador, self, DELAY)
