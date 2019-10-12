import wx

from ui.assets import icons
from ui.app import app


def show(parent):
    icon = wx.Icon(str(icons.CLOUD))
    return SettingsPresenter(SettingsDialog(parent, icon),
                             SettingsInteractor(),
                             app.authService,
                             app.syncDataModel,
                             app.syncManager)


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, icon, title='QuantiSync'):
        super(SettingsDialog, self).__init__(parent, title=title)
        self._initLayout()
        self.SetIcon(icon)

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
        self.btnSelectNfsDir = wx.Button(panel, label="Configurar", size=(100, 25))

        widgetSizer = wx.GridBagSizer(2, 4)
        widgetSizer.Add(self.lblDirNfs, pos=(0, 0))
        widgetSizer.Add(self.txtDirNfs, pos=(1, 0), span=(1, 4), flag=wx.EXPAND, border=5)
        widgetSizer.Add(self.btnSelectNfsDir, pos=(1, 4))

        settingsSizer = wx.BoxSizer(wx.VERTICAL)
        settingsSizer.Add(widgetSizer, wx.SizerFlags(0).Border(wx.ALL, 5))

        panel.SetSizer(settingsSizer)

    def _initAccountTab(self):
        panel = wx.Panel(self.notebook)
        self.notebook.AddPage(panel, "Conta")
        self.btnUnlinkAccount = wx.Button(panel, label="Desvincular conta", size=(150, 25))

        accountSizer = wx.BoxSizer(wx.VERTICAL)
        accountSizer.AddStretchSpacer()
        accountSizer.Add(self.btnUnlinkAccount, wx.SizerFlags(0).Border(wx.ALL, 5))
        accountSizer.AddStretchSpacer()

        panel.SetSizer(accountSizer)

    def showDirNfsDialog(self):
        dlg = wx.DirDialog(self, "Selecione a pasta onde estão localizadas as Notas Fiscais",
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
                           )

        if dlg.ShowModal() == wx.ID_OK:
            self.setDirNfs(dlg.GetPath())

        dlg.Destroy()

    def showUnlinkAccountDialog(self):
        dlg = wx.MessageDialog(self, 'Realmente deseja desvincular este computador?', 'QuantiSync', style=wx.YES_NO)
        confirm = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return confirm

    def getDirNfs(self):
        return self.txtDirNfs.GetValue()

    def setDirNfs(self, dirNfs):
        self.txtDirNfs.SetValue(dirNfs)

    def start(self):
        self.CenterOnScreen()
        self.Raise()
        self.ShowModal()

    def quit(self):
        self.Destroy()


class SettingsPresenter:

    def __init__(self, view, interactor, authService, syncDataModel, syncManager):

        self._view = view
        interactor.Install(self, self._view)
        self._authService = authService
        self._syncDataModel = syncDataModel
        self._syncManager = syncManager
        self._initView()
        self._view.start()

    def _initView(self):
        syncData = self._syncDataModel.getSyncData()
        self._nfsDir = syncData.nfsDir
        self._loadViewFromModel()

    def _loadViewFromModel(self):
        self._view.setDirNfs(self._nfsDir)

    def selectDirNfs(self):
        self._view.showDirNfsDialog()

    def updateModel(self):
        self._nfsDir = self._view.getDirNfs()
        self._syncDataModel.setNfsDir(self._nfsDir)
        self._syncManager.restartSync()
        self._view.quit()

    def unlinkAccount(self):
        confirm = self._view.showUnlinkAccountDialog()
        if confirm:
            self._syncManager.stopSync()
            self._authService.signout()
            self._syncDataModel.remove()
            self._syncManager.cloudFolder.clear()
            self._syncManager.localFolder.clearBlacklistedFolder()
            self._view.quit()


class SettingsInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.btnOk.Bind(wx.EVT_BUTTON, self.OnOk)
        self._view.btnSelectNfsDir.Bind(wx.EVT_BUTTON, self.OnSelectNfsDir)
        self._view.btnUnlinkAccount.Bind(wx.EVT_BUTTON, self.OnUnlinkAccount)

    def OnOk(self, evt):
        self._presenter.updateModel()

    def OnSelectNfsDir(self, evt):
        self._presenter.selectDirNfs()

    def OnUnlinkAccount(self, evt):
        self._presenter.unlinkAccount()
