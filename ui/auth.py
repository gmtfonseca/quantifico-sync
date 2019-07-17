import wx


class AuthDialog(wx.Dialog):

    def __init__(self, parent):
        super(AuthDialog, self).__init__(parent, title='Opções')
        self.parent = parent
        self._initLayout()
        self._controller = AuthController(self)
        self.Show()
        self.CenterOnScreen()

    def _initLayout(self):
        panel = wx.Panel(self)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(notebook, wx.SizerFlags(0).Expand().Border(wx.ALL, 5))

        self._initTabGeral(notebook)
        self._initTabConta(notebook)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnOk = wx.Button(self, wx.ID_OK, label='OK', size=(80, 25))
        btnCancelar = wx.Button(self, wx.ID_CANCEL, label='Cancelar', size=(80, 25))

        btnSizer.Add(btnCancelar, wx.SizerFlags(0).Border(wx.RIGHT | wx.BOTTOM, 5))
        btnSizer.Add(btnOk, wx.SizerFlags(0).Border(wx.RIGHT | wx.BOTTOM, 5))

        mainSizer.Add(btnSizer, wx.SizerFlags(0).Right())
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.OnOk, btnOk)


class AuthController:
    def __init__(self, view):
        self._view = view
