import wx

from quantisync.core.sync import InvalidSettings, Estado
from ui import taskbar
from ui.events import EVT_SYNC
from ui import auth
from ui import settings
from ui import globals


def start():
    return MainPresenter(MainFrame(), MainInteractor())


class MainFrame(wx.Frame):
    '''
    Frame principal responsável pelo TaskBarIcon,
    não possui GUI
    '''

    def __init__(self):
        super(MainFrame, self).__init__(None)
        self._taskBarIcon = taskbar.create(self)

    def getTaskBarIcon(self):
        return self._taskBarIcon


class MainPresenter:
    def __init__(self, view, interactor):
        self._view = view
        interactor.Install(self, self._view)
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
            settings.show(self)

    def updateSyncApp(self, evt):
        if evt.isFatal():
            globals.syncManager.abortSync()

        syncState = evt.getState()
        self.updateTaskBarIcon(syncState)
        self.handleUnauthorized(syncState)

    def handleUnauthorized(self, syncState):
        if syncState == Estado.UNAUTHORIZED:
            auth.show(self)

    def updateTaskBarIcon(self, syncState):
        self._view.getTaskBarIcon().updateView(syncState)


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(EVT_SYNC, self.OnUpdateSyncState)

    def OnUpdateSyncState(self, evt):
        self._presenter.updateSyncApp(evt)
