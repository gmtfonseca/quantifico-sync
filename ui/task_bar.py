import os

from wx.adv import TaskBarIcon
import wx

from ui.options import OptionsDialog
from ui.thread import Estado
from ui.assets import icons, messages


class MainTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        TaskBarIcon.__init__(self)
        icon = wx.Icon(icons.CLOUD.as_posix())
        self.SetIcon(icon, 'QuantiSync')
        self._frame = frame
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.onClickTaskBarIcon)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menuItemConfiguracoes = menu.Append(-1, 'Configurações')
        menu.AppendSeparator()
        menuItemExit = menu.Append(wx.ID_EXIT, 'Sair')

        menu.Bind(wx.EVT_MENU, self.onConfiguracoes, menuItemConfiguracoes)
        menu.Bind(wx.EVT_MENU, self.onSair, menuItemExit)
        return menu

    def onConfiguracoes(self, event):
        self.configuracoesFrame = OptionsDialog(self._frame)
        self.configuracoesFrame.Show()

    def onClickTaskBarIcon(self, evt):
        os.system('start {}'.format(os.path.abspath('../nf')))

    def updateUI(self, estado):
        if (estado == Estado.SYNCING):
            icon = wx.Icon(icons.CLOUD_SYNC.as_posix())
            self.SetIcon(icon, 'Sincronizando...')
        elif (estado == Estado.NORMAL):
            icon = wx.Icon(icons.CLOUD.as_posix())
            self.SetIcon(icon, 'QuantiSync')
        elif (estado == Estado.NO_CONNECTION):
            icon = wx.Icon(icons.CLOUD_OFF.as_posix())
            self.SetIcon(icon, messages.CONNECTION_FAILED)
        elif (estado == Estado.UNAUTHORIZED):
            icon = wx.Icon(icons.CLOUD_OFF.as_posix())
            self.SetIcon(icon, messages.UNAUTHORIZED_USER)

    def onSair(self, event):
        self._frame.backgroundThread.abortar()
        wx.CallAfter(self._frame.Destroy)
        wx.CallAfter(self.Destroy)
