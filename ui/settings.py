import wx

from quantisync.core.settings import SettingsSerializer
from ui import globals


def showDefault(parent):
    return SettingsPresenter(SettingsSerializer(), SettingsDialog(parent), SettingsInteractor())


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, title='Quantifico'):
        super(SettingsDialog, self).__init__(parent, title=title)
        self._initLayout()

    def _initLayout(self):
        self.notebook = wx.Notebook(self)
        self.btnOk = wx.Button(self, wx.ID_OK, label='OK', size=(80, 25))
        self.btnCancelar = wx.Button(self, wx.ID_CANCEL, label='Cancelar', size=(80, 25))

        self._initSettingsTab()
        self._initAccountTab()

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnCancelar, wx.SizerFlags(0).Border(wx.RIGHT | wx.BOTTOM, 5))
        btnSizer.Add(self.btnOk, wx.SizerFlags(0).Border(wx.RIGHT | wx.BOTTOM, 5))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.notebook, wx.SizerFlags(0).Expand().Border(wx.ALL, 5))
        mainSizer.Add(btnSizer, wx.SizerFlags(0).Right())

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def _initSettingsTab(self):
        panel = wx.Panel(self.notebook)
        self.notebook.AddPage(panel, "Configurações")
        self.lblDirNfs = wx.StaticText(panel, label='Selecione a pasta com as Notas Fiscais')
        self.txtDirNfs = wx.TextCtrl(panel, size=(300, 25))
        self.btnConfigurar = wx.Button(panel, label="Configurar", size=(100, 25))

        widgetSizer = wx.GridBagSizer(2, 4)
        widgetSizer.Add(self.lblDirNfs, pos=(0, 0))
        widgetSizer.Add(self.txtDirNfs, pos=(1, 0), span=(1, 4), flag=wx.EXPAND, border=5)
        widgetSizer.Add(self.btnConfigurar, pos=(1, 4))

        settingsSizer = wx.BoxSizer(wx.VERTICAL)
        settingsSizer.Add(widgetSizer, wx.SizerFlags(0).Border(wx.ALL, 5))

        panel.SetSizer(settingsSizer)

    def _initAccountTab(self):
        panel = wx.Panel(self.notebook)
        self.notebook.AddPage(panel, "Conta")
        self.btnDesvincular = wx.Button(panel, label="Desvincular conta", size=(150, 25))

        accountSizer = wx.BoxSizer(wx.VERTICAL)
        accountSizer.AddStretchSpacer()
        accountSizer.Add(self.btnDesvincular, wx.SizerFlags(0).Border(wx.ALL, 5))
        accountSizer.AddStretchSpacer()

        panel.SetSizer(accountSizer)

    def showDirNfsDialog(self):
        dlg = wx.DirDialog(self, "Selecione a pasta onde estão localizadas as Notas Fiscais",
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
                           )

        if dlg.ShowModal() == wx.ID_OK:
            self.setDirNfs(dlg.GetPath())

        dlg.Destroy()

    def getDirNfs(self):
        return self.txtDirNfs.GetValue()

    def setDirNfs(self, dirNfs):
        self.txtDirNfs.SetValue(dirNfs)

    def start(self):
        self.CenterOnScreen()
        self.Show()

    def quit(self):
        self.Destroy()


class SettingsPresenter:

    def __init__(self, settingsSerializer, view, interactor):
        self.settingsSerializer = settingsSerializer
        self._view = view
        interactor.Install(self, self._view)
        self._initView()
        self._view.start()

    def _initView(self):
        self._settings = self.settingsSerializer.load()
        self._loadViewFromModel()

    def _loadViewFromModel(self):
        self._view.setDirNfs(self._settings.nfsDir)

    def selectDirNfs(self):
        self._view.showDirNfsDialog()

    def updateModel(self):
        self._settings.nfsDir = self._view.getDirNfs()
        self.settingsSerializer.save(self._settings)
        globals.syncManager.restartSync()
        self._view.quit()


class SettingsInteractor:

    def Install(self, presenter, view):
        self.presenter = presenter
        self.view = view

        view.btnOk.Bind(wx.EVT_BUTTON, self.OnOk)
        view.btnConfigurar.Bind(wx.EVT_BUTTON, self.OnConfigurar)

    def OnOk(self, evt):
        self.presenter.updateModel()

    def OnConfigurar(self, evt):
        self.presenter.selectDirNfs()
