from pathlib import Path

import wx

from ui import globals
from ui.assets import icons
from quantisync.lib.factory import AuthFactory
from quantisync.core.auth import InvalidUser


class AuthDialog(wx.Dialog):

    def __init__(self, parent):
        super(AuthDialog, self).__init__(parent, title='Quantifico', size=(600, 500))
        icon = wx.Icon(str(icons.CLOUD))
        self.SetIcon(icon)
        self.parent = parent
        self._initLayout()
        self._controller = AuthController(AuthFactory.getKeyringAuth())
        self.Show()
        self.CenterOnScreen()

    def _initLayout(self):
        self.SetBackgroundColour("white")

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.AddStretchSpacer()

        title = wx.StaticText(self, -1, 'Configurar o Quantifico', (20, 120))
        title.SetForegroundColour('#a29bfe')
        font = wx.Font(wx.FontInfo(25).FaceName("Calibri Light"))

        # wx.Font(23, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_EXTRALIGHT)
        title.SetFont(font)
        mainSizer.Add(title, wx.SizerFlags(0).Center().Border(wx.ALL, 5))

        subTitle = wx.StaticText(self, -1, 'Visualize o seu negócio sem complicações e de qualquer lugar.', (20, 120))
        subTitle.SetForegroundColour('#636e72')
        font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        subTitle.SetFont(font)
        mainSizer.Add(subTitle, wx.SizerFlags(0).Center().Border(wx.BOTTOM, 35))

        IMG = Path('ui/assets/images/auth.png')
        png = wx.Image(str(IMG), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        bpm = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
        mainSizer.Add(bpm, wx.SizerFlags(0).Center().Border(wx.ALL, 5))

        self.txtEmail = wx.TextCtrl(self, size=(250, 25))
        self.txtEmail.SetHint('Insira o seu endereço de email')
        mainSizer.Add(self.txtEmail, wx.SizerFlags(0).Center().Border(wx.ALL, 5))

        self.txtPassword = wx.TextCtrl(self, style=wx.TE_PASSWORD, size=(250, 25))
        self.txtPassword.SetHint('Insira a sua senha')
        mainSizer.Add(self.txtPassword, wx.SizerFlags(0).Center().Border(wx.ALL, 5))

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnEntrar = wx.Button(self, label='Entrar', size=(80, 26), style=wx.BORDER_NONE)
        btnEntrar.SetBackgroundColour("#6c5ce7")
        btnEntrar.SetForegroundColour('white')
        btnSizer.Add(btnEntrar, wx.SizerFlags(0).Border(wx.ALL, 5))

        btnCancelar = wx.Button(self, wx.ID_CANCEL, label='Cancelar', size=(80, 26), style=wx.BORDER_NONE)
        btnSizer.Add(btnCancelar, wx.SizerFlags(0).Border(wx.ALL, 5))

        mainSizer.Add(btnSizer, wx.SizerFlags(0).Center().Border(wx.ALL, 5))

        mainSizer.AddStretchSpacer()

        self.SetSizer(mainSizer)
        self.Bind(wx.EVT_BUTTON, self.OnEntrar, btnEntrar)

    def OnEntrar(self, evt):
        try:
            self._controller.signin(self.txtEmail.GetValue(), self.txtPassword.GetValue())
            self.Destroy()
        except InvalidUser:
            dlg = wx.MessageDialog(self, 'Email ou senha inválida',
                                   'Quantifico',
                                   wx.OK | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
            dlg.Destroy()


class AuthController:
    def __init__(self, auth):
        self._auth = auth

    def signin(self, email, password):
        self._auth.signin(email, password)
        globals.syncManager.startSync()
