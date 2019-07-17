import wx

from quantisync.config.storage import CLOUD_SNAPSHOT_PATH
from quantisync.core.options import OptionsSerializer
from quantisync.core.options import Options
from ui import globals


class OptionsDialog(wx.Dialog):

    def __init__(self, parent):
        super(OptionsDialog, self).__init__(parent, title='Opções')
        self.parent = parent
        self._initLayout()
        self._controller = OptionsController(self)
        self._controller.loadOptions()
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

    def OnConfigurar(self, evt):
        dlg = wx.DirDialog(self, "Selecione a pasta onde estão localizadas as Notas Fiscais",
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
                           )

        if dlg.ShowModal() == wx.ID_OK:
            self.txtDirNfs.SetValue(dlg.GetPath())

        dlg.Destroy()

    def OnOk(self, evt):
        self._controller.saveOptions()
        self.Destroy()


class OptionsController:
    def __init__(self, view):
        self._view = view
        self._optionsSerializer = OptionsSerializer()

    def saveOptions(self):
        oldOptions = self._optionsSerializer.load()
        options = Options(self._view.txtDirNfs.GetValue())

        if oldOptions and oldOptions.nfsPath != options.nfsPath and CLOUD_SNAPSHOT_PATH.exists():
            CLOUD_SNAPSHOT_PATH.unlink()

        self._optionsSerializer.save(options)
        globals.syncManager.restartSync()

    def loadOptions(self):
        options = self._optionsSerializer.load()
        self._view.txtDirNfs.SetValue(options.nfsPath)
