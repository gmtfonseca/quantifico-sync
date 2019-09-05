import wx

from quantisync.core.sync import InvalidSettings, State
from ui.events import EVT_SYNC
from ui import taskbar
from ui import auth
from ui import settings
from ui import globals
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
        self._taskBarIcon = taskbar.create(self)

    def showInvalidNfDirDialog(self):
        dlg = wx.MessageDialog(self, 'Informe o diretório onde as Notas Fiscais estão localizadas',
                               'QuantiSync',
                               wx.OK | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def getTaskBarIcon(self):
        return self._taskBarIcon


class MainPresenter:
    def __init__(self, view, interactor):
        self._view = view
        interactor.Install(self, self._view)
        self.startSync()

    def startSync(self):
        try:
            globals.createSyncManager(self._view)
            globals.syncManager.startSync()
        except InvalidSettings:
            self._view.showInvalidNfDirDialog()
            settings.show(self._view)

    async def startSyncAfter(self, delay=60):
        await asyncio.sleep(delay)
        self.startSync()

    def updateSyncApp(self, evt):
        if evt.isFatal():
            globals.syncManager.abortSync()

        syncState = evt.getState()

        self.updateTaskBarIcon(syncState)

        if syncState == State.UNAUTHORIZED:
            auth.show(self._view)

        if syncState == State.NO_CONNECTION:
            asyncio.run(self.startSyncAfter())

    def updateTaskBarIcon(self, syncState):
        self._view.getTaskBarIcon().updateView(syncState)


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(EVT_SYNC, self.OnUpdateSyncState)

    def OnUpdateSyncState(self, evt):
        self._presenter.updateSyncApp(evt)
