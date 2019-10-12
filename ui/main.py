import wx

from quantisync.core.sync import State
from ui.events import EVT_SYNC
from ui.app import app
from ui import taskbar, menu, wizard


def start():
    return MainPresenter(MainFrame(), MainInteractor())


class MainFrame(wx.Frame):
    '''
    Frame principal responsável pelo TaskBarIcon,
    não possui GUI
    '''

    def __init__(self):
        super(MainFrame, self).__init__(None)

    def showInvalidConfigDialog(self):
        dlg = wx.MessageDialog(self, 'Ocorreu um erro ao inicializar a aplicação.',
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
        app.createSyncManager(self._view)
        self._menu = menu.create(self._view)
        self._taskBarIcon = taskbar.create(self._view, self._menu)
        self._initialize()

    def _initialize(self):
        syncData = app.syncDataModel.getSyncData()
        appIsReady = syncData.nfsDir and app.authService.isAuthenticated()

        if appIsReady:
            app.syncManager.startSync()
        else:
            self.updateTaskBarIcon(State.UNAUTHORIZED)
            wizard.show(self._view)

    def update(self, evt):
        syncState = evt.getState()

        self.updateTaskBarIcon(syncState)
        self.updateMenu(syncState)

        if syncState == State.UNAUTHORIZED:
            self._initialize()

    def updateTaskBarIcon(self, syncState):
        self._taskBarIcon.updateView(syncState)

    def updateMenu(self, syncState):
        self._menu.updateState(syncState)

    def removeTaskBarIcon(self):
        if self._taskBarIcon:
            self._taskBarIcon.quit()

    def destroy(self):
        self.removeTaskBarIcon()


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self._view.Bind(EVT_SYNC, self.OnUpdateSyncState)

    def OnUpdateSyncState(self, evt):
        self._presenter.update(evt)

    def OnDestroy(self, evt):
        self._presenter.destroy()
