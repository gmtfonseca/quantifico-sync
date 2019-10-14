import wx
from wx.adv import TaskBarIcon

from quantisync.core.sync import State
from ui.assets import icons, messages


def create(frame, taskBarIconHandler):
    icon = wx.Icon(str(icons.CLOUD))
    return TaskBarPresenter(TaskBarIconView(frame, icon, 'QuantiSync\nAtualizado'),
                            TaskBarInteractor(),
                            taskBarIconHandler)


class TaskBarIconHandler:
    def __init__(self, onSingleLeftClick, onSingleRightClick):
        self.onSingleLeftClick = onSingleLeftClick
        self.onSingleRightClick = onSingleRightClick


class TaskBarIconView(TaskBarIcon):
    def __init__(self, frame, icon, tooltip):
        TaskBarIcon.__init__(self)
        self.setIcon(icon, tooltip)

    def setIcon(self, icon, tooltip):
        self.SetIcon(icon, tooltip)

    def destroy(self):
        wx.CallAfter(self.Destroy)


class TaskBarPresenter:
    def __init__(self, view, interactor, taskBarIconHandler):
        self._view = view
        interactor.Install(self, self._view)
        self._taskBarIconHandler = taskBarIconHandler

    def handleSingleLeftClick(self):
        self._taskBarIconHandler.onSingleLeftClick()

    def handleSingleRightClick(self):
        self._taskBarIconHandler.onSingleRightClick()

    def updateState(self, state):
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

        self._view.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.OnLeftClickTaskBarIcon)
        self._view.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnRightClickTaskBarIcon)

    def OnLeftClickTaskBarIcon(self, evt):
        self._presenter.handleSingleLeftClick()

    def OnRightClickTaskBarIcon(self, evt):
        self._presenter.handleSingleRightClick()
