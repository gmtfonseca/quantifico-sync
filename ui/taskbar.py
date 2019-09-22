import wx
from wx.adv import TaskBarIcon

from quantisync.core.sync import State
from quantisync.core.settings import SettingsSerializer
from ui.assets import icons, messages


def create(frame, menu):
    return TaskBarPresenter(menu,
                            SettingsSerializer(),
                            TaskBarIconView(frame, wx.Icon(str(icons.CLOUD)), 'QuantiSync\nAtualizado'),
                            TaskBarInteractor())


class TaskBarIconView(TaskBarIcon):
    def __init__(self, frame, icon, tooltip):
        TaskBarIcon.__init__(self)
        self.setIcon(icon, tooltip)

    def setIcon(self, icon, tooltip):
        self.SetIcon(icon, tooltip)

    def destroy(self):
        wx.CallAfter(self.Destroy)


class TaskBarPresenter:
    def __init__(self, menu, settingsSerializer, view, interactor):
        self._menu = menu
        self._settingsSerializer = settingsSerializer
        self._view = view
        interactor.Install(self, self._view)

    def showMenu(self):
        self._menu.show()

    def updateView(self, state):
        if (state == State.SYNCING):
            icon = wx.Icon(icons.CLOUD_SYNC.as_posix())
            self._view.setIcon(icon, 'QuantiSync\nSincronizando...')
        elif (state == State.NORMAL):
            icon = wx.Icon(icons.CLOUD.as_posix())
            self._view.setIcon(icon, 'QuantiSync\nAtualizado')
        elif (state == State.NO_CONNECTION):
            icon = wx.Icon(icons.CLOUD_OFF.as_posix())
            self._view.setIcon(icon, messages.CONNECTION_FAILED)
        elif (state == State.UNAUTHORIZED):
            icon = wx.Icon(icons.CLOUD_OFF.as_posix())
            self._view.setIcon(icon, messages.UNAUTHORIZED_USER)

    def quit(self):
        self._view.destroy()


class TaskBarInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnRightClickTaskBarIcon)
        self._view.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.OnLeftClickTaskBarIcon)

    def OnRightClickTaskBarIcon(self, evt):
        self._presenter.showMenu()

    def OnLeftClickTaskBarIcon(self, evt):
        self._presenter.showMenu()
