import wx

from quantisync.core.sync import State
from ui.events import EVT_SYNC
from ui.app import app
from ui import taskbar, menu, wizard, settings
from ui.menu import MenuHandler
from ui.taskbar import TaskBarIconHandler


def start(app):
    return MainPresenter(MainFrame(), MainInteractor(), app)


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
        self.Destroy()


class MainPresenter:
    def __init__(self, view, interactor, app):
        self._view = view
        interactor.Install(self, self._view)
        self._app = app
        self._app.createSyncManager(self._view)
        self._createMenu()
        self._createTaskBarIcon()
        self._activeWindow = None
        self._initialize()

    def _createMenu(self):
        menuHandler = MenuHandler(self.showWizard, self.showConfig, self.quit)
        self._menu = menu.create(self._view,
                                 menuHandler,
                                 self._app.syncDataModel,
                                 self._app.authService,
                                 self._app.syncManager)

    def _createTaskBarIcon(self):
        taskBarIconHandler = TaskBarIconHandler(self.showMenu, self.showMenu)
        self._taskBarIcon = taskbar.create(self._view, taskBarIconHandler)

    def _initialize(self):
        syncData = app.syncDataModel.getSyncData()
        appIsReady = syncData.nfsDir and app.authService.isAuthenticated()

        if appIsReady:
            app.syncManager.startSync()
        else:
            self._taskBarIcon.updateState(State.UNAUTHORIZED)
            self.showWizard()

    def updateChildren(self, evt):
        syncState = evt.getState()

        self._taskBarIcon.updateState(syncState)
        self._menu.updateState(syncState)

        if syncState == State.UNAUTHORIZED:
            self._initialize()

    def showWizard(self):
        window = wizard.create(self._view,
                               self._app.syncDataModel,
                               self._app.authService,
                               self._app.syncManager,
                               self._app.cloudFolder,
                               self._taskBarIcon)
        self._setActiveWindowAndShow(window)

    def showConfig(self):
        window = settings.create(self._view,
                                 self._app.syncDataModel,
                                 self._app.authService,
                                 self._app.syncManager,
                                 self._taskBarIcon)
        self._setActiveWindowAndShow(window)

    def _setActiveWindowAndShow(self, window):
        self._activeWindow = window
        self._activeWindow.show()

    def hasActiveWindow(self):
        return self._activeWindow and self._activeWindow.isActive()

    def showMenu(self):
        if self.hasActiveWindow():
            self._activeWindow.show()
        else:
            self._menu.show()

    def _removeTaskBarIcon(self):
        if self._taskBarIcon:
            self._taskBarIcon.quit()

    def quit(self):
        self._removeTaskBarIcon()
        self._view.destroy()


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(EVT_SYNC, self.OnUpdateSyncState)

    def OnUpdateSyncState(self, evt):
        self._presenter.updateChildren(evt)
