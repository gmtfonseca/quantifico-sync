import wx

from quantisync.core.options import OptionsSerializer
from quantisync.core.options import Options
from quantisync.lib.factory import AuthFactory
from ui import globals

# TODO - Renomear para config / Desacoplar view


class ConfigDialog(wx.Dialog):

    def __init__(self, parent):
        super(ConfigDialog, self).__init__(parent, title='Configurações')
        self.parent = parent
        self._initLayout()
        self._optionsController = OptionsController(self)
        self._optionsController.loadOptions()
        self._accountController = AccountController(AuthFactory.getKeyringAuth())
        self.Show()
        self.CenterOnScreen()

    def _initLayout(self):
        notebook = wx.Notebook(self)

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

    def _initTabGeral(self, notebook):
        panel = wx.Panel(notebook)
        notebook.AddPage(panel, "Geral")

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        widgetSizer = wx.GridBagSizer(2, 4)

        lblDirNfs = wx.StaticText(panel, label='Selecione a pasta com as Notas Fiscais')
        widgetSizer.Add(lblDirNfs, pos=(0, 0))

        self.txtDirNfs = wx.TextCtrl(panel, size=(300, 25))
        widgetSizer.Add(self.txtDirNfs, pos=(1, 0), span=(1, 4), flag=wx.EXPAND, border=5)

        btnConfigurar = wx.Button(panel, label="Configurar", size=(100, 25))
        widgetSizer.Add(btnConfigurar, pos=(1, 4))

        mainSizer.Add(widgetSizer, wx.SizerFlags(0).Border(wx.ALL, 5))

        panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_BUTTON, self.OnConfigurar, btnConfigurar)

    def _initTabConta(self, notebook):
        panel = wx.Panel(notebook)
        notebook.AddPage(panel, "Conta")
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.AddStretchSpacer()
        btnDesvincular = wx.Button(panel, label="Desnvincular conta", size=(150, 25))
        mainSizer.Add(btnDesvincular, wx.SizerFlags(0).Border(wx.ALL, 5))
        mainSizer.AddStretchSpacer()
        panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_BUTTON, self.OnDesvincular, btnDesvincular)

    def OnConfigurar(self, evt):
        dlg = wx.DirDialog(self, "Selecione a pasta onde estão localizadas as Notas Fiscais",
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
                           )

        if dlg.ShowModal() == wx.ID_OK:
            self.txtDirNfs.SetValue(dlg.GetPath())

        dlg.Destroy()

    def OnDesvincular(self, evt):
        dlg = wx.MessageDialog(self, 'Realmente deseja desvincular este computador?', 'Quantifico', style=wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            self._accountController.unlinkAccount()

    def OnOk(self, evt):
        self._optionsController.saveOptions()
        self.Destroy()


class OptionsController:
    def __init__(self, view):
        self._view = view
        self._optionsSerializer = OptionsSerializer()

    def saveOptions(self):
        options = Options(self._view.txtDirNfs.GetValue())
        self._optionsSerializer.save(options)
        globals.syncManager.restartSync()

    def loadOptions(self):
        options = self._optionsSerializer.load()
        self._view.txtDirNfs.SetValue(options.nfsPath)


class AccountController:
    def __init__(self, auth):
        self._auth = auth

    def unlinkAccount(self):
        self._auth.signout()
