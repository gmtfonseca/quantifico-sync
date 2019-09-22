import wx

from quantisync.config import storage
from quantisync.lib.factory import SyncFactory
from quantisync.core.sync import InvalidSettings, State
from quantisync.core.snapshot import BlacklistedFolder, CloudFolder
from ui.events import EVT_SYNC
from ui import taskbar, menu, auth, settings, globals
import asyncio


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
        cloudFolder = CloudFolder(storage.CLOUD_FOLDER_PATH)
        blacklistedFolder = BlacklistedFolder(storage.BLACKLISTED_FOLDER_PATH)
        self._menu = menu.create(self._view, cloudFolder, blacklistedFolder)
        self._taskBarIcon = taskbar.create(self._view, self._menu)
        self.createSync(cloudFolder, blacklistedFolder)
        self.startSync()

    def createSync(self, cloudFolder, blacklistedFolder):
        syncFactory = SyncFactory(self._view, cloudFolder, blacklistedFolder)
        try:
            globals.createSyncManager(syncFactory)
        except InvalidSettings:
            self._view.showInvalidNfDirDialog()
            settings.show(self._view)

    def startSync(self):
        globals.syncManager.startSync()

    async def startSyncAfter(self, delay=60):
        await asyncio.sleep(delay)
        self.startSync()

    def updateSyncApp(self, evt):
        if evt.isFatal():
            globals.syncManager.abortSync()

        syncState = evt.getState()

        self.updateTaskBarIcon(syncState)
        self.updateMenu(syncState)

        if syncState == State.UNAUTHORIZED:
            auth.show(self._view)

        # if syncState == State.NO_CONNECTION:
            # asyncio.run(self.startSyncAfter())

    def updateTaskBarIcon(self, syncState):
        self._taskBarIcon.updateView(syncState)

    def updateMenu(self, syncState):
        self._menu.updateModel(syncState)

    def removeTaskBarIcon(self):
        self._taskBarIcon.quit()


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self._view.Bind(EVT_SYNC, self.OnUpdateSyncState)

    def OnUpdateSyncState(self, evt):
        self._presenter.updateSyncApp(evt)

    def OnDestroy(self, evt):
        globals.syncManager.abortSync()
        self._presenter.removeTaskBarIcon()
