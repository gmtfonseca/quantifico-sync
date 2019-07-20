import wx

from quantisync.core.sync import InvalidSettings, Estado
from quantisync.core.settings import SettingsSerializer
from ui.task_bar import MainTaskBarIcon
from ui.events import EVT_UI
from ui.auth import AuthDialog
from ui import settings
from ui import globals


class MainFrame(wx.Frame):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.Bind(EVT_UI, self.OnUpdate)
        self.taskBarIcon = MainTaskBarIcon(self)
        self.startSync()
        settings.SettingsPresenter(SettingsSerializer(), settings.SettingsDialog(self), settings.SettingsInteractor())

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
            # configDialog = ConfigDialog(self)
            # configDialog.ShowModal()

    def OnUpdate(self, evt):
        if evt.isFatal():
            globals.syncManager.abortSync()

        estadoSync = evt.getEstado()
        self.taskBarIcon.updateView(estadoSync)

        if estadoSync == Estado.UNAUTHORIZED:
            authDialog = AuthDialog(self)
            authDialog.ShowModal()
