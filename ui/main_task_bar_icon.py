from wx.adv import TaskBarIcon
import wx
from .cliente_config_dialog import ClienteConfigDialog


class MainTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        TaskBarIcon.__init__(self)
        icon = wx.Icon('F:/Projetos/quantifico/quantifico-sync/ui/images/icons/quantifico.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon, 'QuantiSync')
        self._frame = frame

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

    def onSair(self, event):
        self._frame.loopThread.abort()
        wx.CallAfter(self._frame.Destroy)
        wx.CallAfter(self.Destroy)
