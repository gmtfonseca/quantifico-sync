import wx

from quantisync.core.sync import State, InvalidSyncSettings
from ui.events import EVT_SYNC
from ui.app import app
from ui import taskbar, menu, auth, settings


def start():
    return MainPresenter(MainFrame(), MainInteractor())


class MainFrame(wx.Frame):
    '''
    Frame principal responsável pelo TaskBarIcon,
    não possui GUI
    '''

    def __init__(self):
        super(MainFrame, self).__init__(None)

    def showInvalidNfDirDialog(self):
        dlg = wx.MessageDialog(self, 'Informe o diretório onde as Notas Fiscais estão localizadas',
                               'QuantiSync',
                               wx.OK | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def destroy(self):
        wx.CallAfter(self.Destroy)


class MainPresenter:
    def __init__(self, view, interactor):
        self._view = view
        interactor.Install(self, self._view)
        self.createSyncAndStart()
        self._menu = menu.create(self._view)
        self._taskBarIcon = taskbar.create(self._view, self._menu)

    def createSyncAndStart(self):
        try:
            app.createSyncManager(self._view)
            app.syncManager.startSync()
        except InvalidSyncSettings:
            self._view.showInvalidNfDirDialog()
            settings.show(self._view)

    def updateSyncApp(self, evt):
        syncState = evt.getState()

        self.updateTaskBarIcon(syncState)
        self.updateMenu(syncState)

        if syncState == State.UNAUTHORIZED:
            auth.show(self._view)

    def updateTaskBarIcon(self, syncState):
        self._taskBarIcon.updateView(syncState)

    def updateMenu(self, syncState):
        self._menu.updateState(syncState)

    def removeTaskBarIcon(self):
        self._taskBarIcon.quit()

    def destroy(self):
        app.syncManager.stopSync()
        self.removeTaskBarIcon()


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self._view.Bind(EVT_SYNC, self.OnUpdateSyncState)

    def OnUpdateSyncState(self, evt):
        self._presenter.updateSyncApp(evt)

    def OnDestroy(self, evt):
        self._presenter.destroy()
