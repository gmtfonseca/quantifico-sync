import wx

from quantisync.core.sync import InvalidOptions
from ui.task_bar import MainTaskBarIcon
from ui.events import EVT_UI
from ui.options import OptionsDialog
from ui import globals
# Teste
# from ui.auth import AuthDialog


class MainFrame(wx.Frame):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.Bind(EVT_UI, self.OnUpdate)
        self.taskBarIcon = MainTaskBarIcon(self)
        self.startSync()

    def startSync(self):
        try:
            globals.createSyncManager(self)
            globals.syncManager.startSync()
        except InvalidOptions:
            dlg = wx.MessageDialog(self, 'Informe o diretório onde as Notas Fiscais estão localizadas',
                                   'QuantiSync',
                                   wx.OK | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            optionsDialog = OptionsDialog(self)
            optionsDialog.ShowModal()

    def OnUpdate(self, evt):
        if evt.isFatal():
            globals.syncManager.abortSync()

        self.taskBarIcon.updateView(evt.getEstado())
