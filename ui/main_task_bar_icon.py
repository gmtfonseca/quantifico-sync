from .cliente_config_dialog import ClienteConfigDialog
from wx.adv import TaskBarIcon
from modules.loop_thread import Estado
import wx
import os


class MainTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        TaskBarIcon.__init__(self)
        icon = wx.Icon('F:/Projetos/quantifico/quantifico-sync/ui/images/icons/cloud.ico', wx.BITMAP_TYPE_ICO)
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
        self.configuracoesFrame = ClienteConfigDialog(self._frame)
        self.configuracoesFrame.Show()

    def onClickTaskBarIcon(self, evt):
        os.system('start {}'.format(os.path.abspath('../nf')))

    def updateUI(self, estado):
        if (estado == Estado.SYNCING):
            icon = wx.Icon('F:/Projetos/quantifico/quantifico-sync/ui/images/icons/cloud-sync.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)
        elif (estado == Estado.NORMAL):
            icon = wx.Icon('F:/Projetos/quantifico/quantifico-sync/ui/images/icons/cloud.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon, 'QuantiSync')

    def onSair(self, event):
        self._frame.loopThread.abort()
        wx.CallAfter(self._frame.Destroy)
        wx.CallAfter(self.Destroy)
