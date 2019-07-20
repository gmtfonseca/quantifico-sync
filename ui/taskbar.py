import os

import wx
from wx.adv import TaskBarIcon

from quantisync.core.sync import Estado
from quantisync.core.settings import SettingsSerializer
from ui.assets import icons, messages
from ui import settings
from ui import globals


def getDefault(frame):
    return TaskBarPresenter(SettingsSerializer(),
                            TaskBarIconView(frame, wx.Icon(str(icons.CLOUD)), 'Quantifico\nAtualizado'),
                            TaskBarInteractor())


class TaskBarIconView(TaskBarIcon):
    def __init__(self, frame, icon, tooltip):
        TaskBarIcon.__init__(self)
        self._frame = frame
        self._createPopupMenu()
        self.setIcon(icon, tooltip)

    def _createPopupMenu(self):
        self.popupMenu = wx.Menu()
        self.menuItemSettings = self.popupMenu.Append(-1, 'Configurações')
        self.popupMenu.AppendSeparator()
        self.menuItemExit = self.popupMenu.Append(wx.ID_EXIT, 'Sair')

    def setIcon(self, icon, tooltip):
        self.SetIcon(icon, tooltip)

    def getFrame(self):
        return self._frame

    def destroy(self):
        wx.CallAfter(self._frame.Destroy)
        wx.CallAfter(self.Destroy)


class TaskBarPresenter:
    def __init__(self, settingsSerializer, view, interactor):
        self._view = view
        self._settingsSerializer = settingsSerializer
        interactor.Install(self, self._view)

    def showSettings(self):
        settings.showDefault(self._view.getFrame())

    def showPopupMenu(self):
        self._view.PopupMenu(self._view.popupMenu)

    def openSyncFolder(self):
        settings = self._settingsSerializer.load()
        os.system('start {}'.format(settings.nfsDir))

    def updateView(self, state):
        if (state == Estado.SYNCING):
            icon = wx.Icon(icons.CLOUD_SYNC.as_posix())
            self._view.setIcon(icon, 'Quantifico\nSincronizando...')
        elif (state == Estado.NORMAL):
            icon = wx.Icon(icons.CLOUD.as_posix())
            self._view.setIcon(icon, 'Quantifico\nAtualizado')
        elif (state == Estado.NO_CONNECTION):
            icon = wx.Icon(icons.CLOUD_OFF.as_posix())
            self._view.setIcon(icon, messages.CONNECTION_FAILED)
        elif (state == Estado.UNAUTHORIZED):
            icon = wx.Icon(icons.CLOUD_OFF.as_posix())
            self._view.setIcon(icon, messages.UNAUTHORIZED_USER)

    def quit(self):
        globals.syncManager.abortSync()
        self._view.destroy()


class TaskBarInteractor:

    def Install(self, presenter, view):
        self.presenter = presenter
        self.view = view

        view.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnRightClickTaskBarIcon)
        view.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.OnLeftClickTaskBarIcon)
        view.popupMenu.Bind(wx.EVT_MENU, self.OnConfiguracoes, view.menuItemSettings)
        view.popupMenu.Bind(wx.EVT_MENU, self.OnSair, view.menuItemExit)

    def OnRightClickTaskBarIcon(self, evt):
        self.presenter.showPopupMenu()

    def OnLeftClickTaskBarIcon(self, evt):
        self.presenter.openSyncFolder()

    def OnConfiguracoes(self, evt):
        self.presenter.showSettings()

    def OnSair(self, evt):
        self.presenter.quit()
