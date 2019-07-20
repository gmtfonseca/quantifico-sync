import wx

from quantisync.core.sync import InvalidSettings, Estado
from ui import taskbar
from ui.events import EVT_UI
from ui.auth import AuthDialog
from ui import settings
from ui import globals


class MainFrame(wx.Frame):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.Bind(EVT_UI, self.OnUpdate)
        self.taskBarIcon = taskbar.getDefault(self)
        self.startSync()

    def startSync(self):
        try:
            globals.createSyncManager(self)
            globals.syncManager.startSync()
        except InvalidSettings:
            dlg = wx.MessageDialog(self, 'Informe o diretório onde as Notas Fiscais estão localizadas',
                                   'Quantifico',
                                   wx.OK | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            settings.showDefault(self)

    def OnUpdate(self, evt):
        if evt.isFatal():
            globals.syncManager.abortSync()

        estadoSync = evt.getEstado()
        self.taskBarIcon.updateView(estadoSync)

        if estadoSync == Estado.UNAUTHORIZED:
            authDialog = AuthDialog(self)
            authDialog.ShowModal()
