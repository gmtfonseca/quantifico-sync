import wx

from ui.task_bar import MainTaskBarIcon
from ui.events import EVT_UI
from ui import globals

# from ui.options import OptionsDialog


class MainFrame(wx.Frame):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.Bind(EVT_UI, self.OnUpdate)
        self.taskBarIcon = MainTaskBarIcon(self)

        globals.createSyncManager(self)
        globals.syncManager.startSync()

    def OnUpdate(self, evt):
        if evt.isFatal():
            globals.syncManager.abortSync()

        self.taskBarIcon.updateView(evt.getEstado())
