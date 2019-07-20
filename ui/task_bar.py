import os

from wx.adv import TaskBarIcon
import wx

from quantisync.core.sync import Estado
from ui.config import ConfigDialog
from ui.assets import icons, messages
from ui import globals


class MainTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        TaskBarIcon.__init__(self)
        icon = wx.Icon(icons.CLOUD.as_posix())
        self.SetIcon(icon, 'Quantifico\nAtualizado')
        self._frame = frame
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.OnClickTaskBarIcon)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menuItemConfiguracoes = menu.Append(-1, 'Configurações')
        menu.AppendSeparator()
        menuItemExit = menu.Append(wx.ID_EXIT, 'Sair')

        menu.Bind(wx.EVT_MENU, self.OnConfiguracoes, menuItemConfiguracoes)
        menu.Bind(wx.EVT_MENU, self.OnSair, menuItemExit)
        return menu

    def OnConfiguracoes(self, event):
        self.configuracoesFrame = ConfigDialog(self._frame)
        self.configuracoesFrame.Show()

    def OnClickTaskBarIcon(self, evt):
        os.system('start {}'.format(os.path.abspath('../nf')))

    def OnSair(self, event):
        globals.syncManager.abortSync()
        wx.CallAfter(self._frame.Destroy)
        wx.CallAfter(self.Destroy)

    def updateView(self, estado):
        if (estado == Estado.SYNCING):
            icon = wx.Icon(icons.CLOUD_SYNC.as_posix())
            self.SetIcon(icon, 'Quantifico\nSincronizando...')
        elif (estado == Estado.NORMAL):
            icon = wx.Icon(icons.CLOUD.as_posix())
            self.SetIcon(icon, 'Quantifico\nAtualizado')
        elif (estado == Estado.NO_CONNECTION):
            icon = wx.Icon(icons.CLOUD_OFF.as_posix())
            self.SetIcon(icon, messages.CONNECTION_FAILED)
        elif (estado == Estado.UNAUTHORIZED):
            icon = wx.Icon(icons.CLOUD_OFF.as_posix())
            self.SetIcon(icon, messages.UNAUTHORIZED_USER)
