from pathlib import Path

import wx

from ui import globals
from ui.assets import icons
from quantisync.lib.factory import AuthFactory
from quantisync.core.auth import InvalidUser


def showDefault(parent):
    icon = wx.Icon(str(icons.CLOUD))
    return AuthPresenter(AuthFactory.getKeyringAuth(),
                         AuthDialog(parent, 'Quantifico', icon=icon),
                         AuthInteractor())


class AuthDialog(wx.Dialog):

    def __init__(self, parent, title, icon):
        super(AuthDialog, self).__init__(parent, title=title, size=(600, 500))
        self.SetIcon(icon)
        self._initLayout()

    def _initLayout(self):
        self.SetBackgroundColour("white")

        title = wx.StaticText(self, -1, 'Configurar o Quantifico', (20, 120))
        title.SetForegroundColour('#a29bfe')
        font = wx.Font(wx.FontInfo(25).FaceName("Calibri Light"))
        title.SetFont(font)

        subTitle = wx.StaticText(self, -1, 'Visualize o seu negócio sem complicações e de qualquer lugar.', (20, 120))
        subTitle.SetForegroundColour('#636e72')
        font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        subTitle.SetFont(font)

        IMG = Path('ui/assets/images/auth.png')
        png = wx.Image(str(IMG), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        bpm = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        self.txtEmail = wx.TextCtrl(self, size=(250, 25))
        self.txtEmail.SetHint('Insira o seu endereço de email')

        self.txtPassword = wx.TextCtrl(self, style=wx.TE_PASSWORD, size=(250, 25))
        self.txtPassword.SetHint('Insira a sua senha')

        self.btnSignin = wx.Button(self, label='Entrar', size=(80, 26), style=wx.BORDER_NONE)
        self.btnSignin.SetBackgroundColour("#6c5ce7")
        self.btnSignin.SetForegroundColour('white')

        self.btnCancel = wx.Button(self, wx.ID_CANCEL, label='Cancelar', size=(80, 26), style=wx.BORDER_NONE)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnSignin, wx.SizerFlags(0).Border(wx.ALL, 5))
        btnSizer.Add(self.btnCancel, wx.SizerFlags(0).Border(wx.ALL, 5))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(title, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(subTitle, wx.SizerFlags(0).Center().Border(wx.BOTTOM, 35))
        mainSizer.Add(bpm, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(self.txtEmail, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(self.txtPassword, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(btnSizer, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.AddStretchSpacer()

        self.SetSizer(mainSizer)

    def showInvalidUserDialog(self):
        dlg = wx.MessageDialog(self, 'Email ou senha inválida',
                               'Quantifico',
                               wx.OK | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def getEmail(self):
        return self.txtEmail.GetValue()

    def getPassword(self):
        return self.txtPassword.GetValue()

    def quit(self):
        self.Destroy()

    def start(self):
        self.Show()
        self.CenterOnScreen()


class AuthPresenter:
    def __init__(self, auth, view, interactor):
        self._auth = auth
        self._view = view
        interactor.Install(self, self._view)
        self._view.start()

    def signinAndStartSync(self):
        try:
            self._auth.signin(self._view.getEmail(), self._view.getPassword())
            globals.syncManager.startSync()
            self._view.quit()
        except InvalidUser:
            self._view.showInvalidUserDialog()


class AuthInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.btnSignin.Bind(wx.EVT_BUTTON, self.OnSignin)

    def OnSignin(self, evt):
        self._presenter.signinAndStartSync()