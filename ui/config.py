from enum import Enum

import wx

from quantisync.core.sync import State

from ui.assets import icons, colors
from ui.components import widgets


class Tab(Enum):
    '''
    Representa uma tab da tela de preferências
    '''
    CONFIG = 0
    ACCOUNT = 1


def create(parent, syncDataModel, authService, syncManager, taskBarIcon):
    icon = wx.Icon(str(icons.CLOUD))
    return ConfigPresenter(ConfigFrame(parent, icon),
                           ConfigInteractor(),
                           syncDataModel,
                           authService,
                           syncManager,
                           taskBarIcon)


class ConfigFrame(wx.Frame):

    def __init__(self, parent, icon, title='Preferências de sincronização do Quantifico'):
        super(ConfigFrame, self).__init__(parent, title=title,
                                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_NO_TASKBAR,
                                          size=(800, 600))
        self.SetIcon(icon)
        self._initLayout()

    def _initLayout(self):
        self.SetBackgroundColour(wx.WHITE)

        windowWidth, windowHeight = self.GetSize()

        menuWidth = windowWidth * 0.25
        self.menu = self._initMenu(menuWidth, windowHeight)

        footerWidth = windowWidth - self.menu.GetSize()[0]
        footerHeight = windowHeight * 0.17
        self.footer = self._initFooter(footerWidth, footerHeight)

        contentWidth = windowWidth - self.menu.GetSize()[0]
        contentHeight = windowHeight - self.footer.GetSize()[1]
        self.configPanel = self._initConfigPanel(contentWidth, contentHeight)
        self.accountPanel = self._initAccountPanel(contentWidth, contentHeight)

        hMainSizer = wx.BoxSizer(wx.HORIZONTAL)
        hMainSizer.Add(self.menu)

        vMainSizer = wx.BoxSizer(wx.VERTICAL)
        vMainSizer.Add(self.configPanel, wx.SizerFlags(0).Border(wx.LEFT | wx.RIGHT, 25))
        vMainSizer.Add(self.accountPanel, wx.SizerFlags(0).Border(wx.LEFT | wx.RIGHT, 25))
        vMainSizer.Add(self.footer)
        hMainSizer.Add(vMainSizer)
        self.SetSizer(hMainSizer)

    def _initMenu(self, width, height):
        panel = wx.Panel(self, style=wx.NO_BORDER, size=(width, height))
        panel.SetBackgroundColour(colors.GREY_VERY_LIGHT)

        font = wx.Font(wx.FontInfo(10).Bold())

        # Config tab
        self.configTab = wx.Panel(panel, id=Tab.CONFIG.value, style=wx.NO_BORDER, size=(width, 60))

        pngConfig = wx.Image(str(icons.ONE), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bmpConfig = wx.StaticBitmap(self.configTab, Tab.CONFIG.value, pngConfig,
                                         size=(pngConfig.GetWidth(), pngConfig.GetHeight()))

        self.txtConfig = wx.StaticText(self.configTab, Tab.CONFIG.value, 'Configurações')
        self.txtConfig.SetFont(font)

        vConfigTabSizer = wx.BoxSizer(wx.VERTICAL)
        hConfigTabSizer = wx.BoxSizer(wx.HORIZONTAL)
        hConfigTabSizer.Add(self.bmpConfig, 0, wx.CENTER)
        hConfigTabSizer.Add(self.txtConfig, wx.SizerFlags(0).Center().Border(wx.LEFT, 10))
        vConfigTabSizer.Add(hConfigTabSizer, wx.SizerFlags(1).Left().Border(wx.LEFT, 25))

        self.configTab.SetSizer(vConfigTabSizer)

        # Account tab
        self.accountTab = wx.Panel(panel, id=Tab.ACCOUNT.value, style=wx.NO_BORDER, size=(width, 60))

        pngAccount = wx.Image(str(icons.TWO), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bmpAccount = wx.StaticBitmap(self.accountTab, Tab.ACCOUNT.value, pngAccount,
                                          size=(pngAccount.GetWidth(), pngAccount.GetHeight()))

        self.txtAccount = wx.StaticText(self.accountTab, Tab.ACCOUNT.value, 'Minha conta')
        self.txtAccount.SetFont(font)

        vAccountTabSizer = wx.BoxSizer(wx.VERTICAL)
        hAccountTabSizer = wx.BoxSizer(wx.HORIZONTAL)
        hAccountTabSizer.Add(self.bmpAccount, 1, wx.CENTER)
        hAccountTabSizer.Add(self.txtAccount, wx.SizerFlags(0).Center().Border(wx.LEFT, 10))

        vAccountTabSizer.Add(hAccountTabSizer, wx.SizerFlags(1).Left().Border(wx.LEFT, 25))
        self.accountTab.SetSizer(vAccountTabSizer)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.configTab, wx.SizerFlags(0).Border(wx.TOP, 30))
        mainSizer.Add(self.accountTab, wx.SizerFlags(0).Expand())
        panel.SetSizer(mainSizer)

        return panel

    def _initConfigPanel(self, width, height):
        panel = wx.Panel(self, size=(width, height))
        panel.SetBackgroundColour(wx.WHITE)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, -1, 'Configurações')
        font = wx.Font(wx.FontInfo(13).Bold())
        title.SetFont(font)

        nfsDirFont = wx.Font(wx.FontInfo(10))
        lblNfsDir = wx.StaticText(panel, -1, 'Localização da pasta com as Notas Fiscais:')
        lblNfsDir.SetFont(nfsDirFont)

        self.txtNfsDir = wx.StaticText(panel, -1, '')
        self.txtNfsDir.SetFont(nfsDirFont)
        self.txtNfsDir.SetForegroundColour(colors.GREY)

        self.nfsDir = wx.GenericDirCtrl(panel, -1, size=(-1, 380), style=wx.DIRCTRL_DIR_ONLY)

        nfsPathSizer = wx.BoxSizer(wx.HORIZONTAL)
        nfsPathSizer.Add(lblNfsDir, wx.SizerFlags(0))
        nfsPathSizer.Add(self.txtNfsDir, wx.SizerFlags(0).Border(wx.LEFT, 5))

        nfsDirSizer = wx.BoxSizer(wx.HORIZONTAL)
        nfsDirSizer.Add(self.nfsDir, wx.SizerFlags(1).Expand().Border(wx.TOP, 15))

        mainSizer.Add(title, wx.SizerFlags(0).Border(wx.TOP, 35))
        mainSizer.Add(nfsPathSizer, wx.SizerFlags(0).Expand().Border(wx.TOP, 25))
        mainSizer.Add(nfsDirSizer, wx.SizerFlags(0).Expand())

        panel.SetSizer(mainSizer)

        return panel

    def _initAccountPanel(self, width, height):
        panel = wx.Panel(self, size=(width, height))
        panel.SetBackgroundColour(wx.WHITE)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, -1, 'Minha conta')
        font = wx.Font(wx.FontInfo(13).Bold())
        title.SetFont(font)

        userFont = wx.Font(wx.FontInfo(10))
        self.txtEmail = wx.StaticText(panel, -1, '')
        self.txtEmail.SetFont(userFont)
        self.txtEmail.SetForegroundColour(colors.GREY)

        self.txtOrg = wx.StaticText(panel, -1, '')
        self.txtOrg.SetFont(userFont)

        self.btnUnlinkAccount = widgets.SecondaryButton(panel, 'DESCONECTAR CONTA', size=(125, 30))

        mainSizer.Add(title, wx.SizerFlags(0).Border(wx.TOP, 35))
        mainSizer.Add(self.txtOrg, wx.SizerFlags(0).Border(wx.TOP, 25))
        mainSizer.Add(self.txtEmail, wx.SizerFlags(0).Border(wx.TOP, 5))
        mainSizer.Add(self.btnUnlinkAccount, wx.SizerFlags(0).Border(wx.TOP, 25))

        panel.SetSizer(mainSizer)

        return panel

    def _initFooter(self, width, height):
        panel = wx.Panel(self, size=(width, height))
        panel.SetBackgroundColour(wx.WHITE)

        self.btnOk = widgets.PrimaryButton(panel,  'OK')
        self.btnCancel = widgets.SecondaryButton(panel,  'CANCELAR')

        vMainSizer = wx.BoxSizer(wx.VERTICAL)
        hMainSizer = wx.BoxSizer(wx.HORIZONTAL)
        hMainSizer.Add(self.btnCancel, wx.SizerFlags(0).Border(wx.TOP | wx.BOTTOM | wx.RIGHT, 10))
        hMainSizer.Add(self.btnOk, wx.SizerFlags(0).Border(wx.TOP | wx.BOTTOM, 10))
        vMainSizer.Add(hMainSizer, wx.SizerFlags(0).Right().Border(wx.RIGHT, 25))
        panel.SetSizer(vMainSizer)

        return panel

    def showUnlinkAccountDialog(self):
        dlg = wx.MessageDialog(self, 'Realmente deseja desconectar este usuário deste computador?',
                               'Quantifico', style=wx.YES_NO)
        confirm = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return confirm

    def start(self):
        self.Raise()
        self.Show()

    def destroy(self):
        self.Destroy()


class ConfigPresenter:

    def __init__(self, view, interactor, syncDataModel, authService, syncManager, taskBarIcon):

        self._view = view
        self._view.CenterOnScreen()
        interactor.Install(self, self._view)
        self._syncDataModel = syncDataModel
        self._authService = authService
        self._syncManager = syncManager
        self._taskBarIcon = taskBarIcon
        self._initView()

    def _initView(self):
        self._currTab = Tab.CONFIG
        syncData = self._syncDataModel.getSyncData()
        self._nfsDir = syncData.nfsDir
        self._userOrg = syncData.userOrg
        self._userEmail = syncData.userEmail
        self._loadViewFromModel()
        self._showCurrTab()

    def _loadViewFromModel(self):
        self._view.txtNfsDir.SetLabel(self._nfsDir)
        self._view.nfsDir.ExpandPath(self._nfsDir)
        self._view.nfsDir.SelectPath(self._nfsDir)
        self._view.txtOrg.SetLabel(self._userOrg)
        self._view.txtEmail.SetLabel(self._userEmail)
        self._view.Layout()
        self._view.Refresh()

    def _switchTab(self, tab):
        self._currTab = tab
        self._showCurrTab()

    def _showCurrTab(self):
        if self._currTab == Tab.CONFIG:
            self._selectConfigTab()
            self._showConfigTab()
        elif self._currTab == Tab.ACCOUNT:
            self._selectAccountTab()
            self._showAccountTab()

    def _showConfigTab(self):
        self._view.accountPanel.Hide()
        self._view.configPanel.Show()
        self._view.Layout()
        self._view.Refresh()

    def _showAccountTab(self):
        self._view.accountPanel.Show()
        self._view.configPanel.Hide()
        self._view.Layout()
        self._view.Refresh()

    def _selectConfigTab(self):
        bmpConfig = wx.Image(str(icons.CONFIG_FOCUSED), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._view.bmpConfig.SetBitmap(bmpConfig)
        self._view.configTab.SetBackgroundColour(colors.GREY_LIGHT)
        self._view.txtConfig.SetForegroundColour(colors.PRIMARY)

        bmpAccount = wx.Image(str(icons.USER), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._view.bmpAccount.SetBitmap(bmpAccount)
        self._view.accountTab.SetBackgroundColour(colors.GREY_VERY_LIGHT)
        self._view.txtAccount.SetForegroundColour(wx.BLACK)

    def _selectAccountTab(self):
        bmpAccount = wx.Image(str(icons.USER_FOCUSED), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._view.bmpAccount.SetBitmap(bmpAccount)
        self._view.accountTab.SetBackgroundColour(colors.GREY_LIGHT)
        self._view.txtAccount.SetForegroundColour(colors.PRIMARY)

        bmpConfig = wx.Image(str(icons.CONFIG), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._view.bmpConfig.SetBitmap(bmpConfig)
        self._view.configTab.SetBackgroundColour(colors.GREY_VERY_LIGHT)
        self._view.txtConfig.SetForegroundColour(wx.BLACK)

    def updateModel(self):
        self._nfsDir = self._view.nfsDir.GetPath()
        self._loadViewFromModel()

    def _restartSync(self):
        try:
            self._syncManager.restartSync()
            self._taskBarIcon.updateState(State.NORMAL)
        except Exception as err:
            print(err)
            raise err

    def confirmUnlinkAccount(self):
        confirm = self._view.showUnlinkAccountDialog()
        if confirm:
            self._unlinkAccount()
            self.quit()

    def _unlinkAccount(self):
        try:
            self._syncManager.stopSync()
            self._authService.signout()
            self._syncDataModel.remove()
            self._syncManager.cloudFolder.clear()
            self._syncManager.localFolder.clearBlacklistedFolder()
            self._taskBarIcon.updateState(State.UNAUTHORIZED)
        except Exception as err:
            print(err)
            raise err

    def handleMenu(self, evt):
        if evt.GetId() == Tab.CONFIG.value:
            self._switchTab(Tab.CONFIG)
        elif evt.GetId() == Tab.ACCOUNT.value:
            self._switchTab(Tab.ACCOUNT)

    def confirmChanges(self, evt):
        self.updateModel()
        self._syncDataModel.setNfsDir(self._nfsDir)
        self._restartSync()
        self.quit()

    def isActive(self):
        return bool(self._view)

    def show(self):
        self._view.start()

    def quit(self):
        self._view.destroy()


class ConfigInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self._view.btnOk.Bind(wx.EVT_BUTTON, self.OnOk)
        self._view.btnUnlinkAccount.Bind(wx.EVT_BUTTON, self.OnUnlinkAccount)
        self._view.nfsDir.Bind(wx.EVT_DIRCTRL_SELECTIONCHANGED, self.OnNfsDirChange)

        self._view.configTab.Bind(wx.EVT_LEFT_DOWN, self.OnClickMenuTab)
        self._view.bmpConfig.Bind(wx.EVT_LEFT_DOWN, self.OnClickMenuTab)
        self._view.txtConfig.Bind(wx.EVT_LEFT_DOWN, self.OnClickMenuTab)

        self._view.accountTab.Bind(wx.EVT_LEFT_DOWN, self.OnClickMenuTab)
        self._view.bmpAccount.Bind(wx.EVT_LEFT_DOWN, self.OnClickMenuTab)
        self._view.txtAccount.Bind(wx.EVT_LEFT_DOWN, self.OnClickMenuTab)

    def OnCancel(self, evt):
        self._presenter.quit()

    def OnClickMenuTab(self, evt):
        self._presenter.handleMenu(evt)

    def OnOk(self, evt):
        self._presenter.confirmChanges(evt)

    def OnSelectNfsDir(self, evt):
        self._presenter.selectDirNfs()

    def OnNfsDirChange(self, evt):
        self._presenter.updateModel()

    def OnUnlinkAccount(self, evt):
        self._presenter.confirmUnlinkAccount()
