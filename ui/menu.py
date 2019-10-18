import wx
import os
from datetime import datetime

from ui import blacklist
from ui.assets import icons, colors
from ui.components import widgets

from quantisync.core.sync import State
from quantisync.lib.util import DeltaTime


def create(parent, menuHandler, syncDataModel, authService, syncManager):
    return MenuPresenter(MenuFrame(parent),
                         MenuInteractor(),
                         menuHandler,
                         syncDataModel,
                         authService,
                         syncManager)


class MenuHandler:
    def __init__(self, onSignin, onConfig, onExit):
        self.onSignin = onSignin
        self.onConfig = onConfig
        self.onExit = onExit


class MenuFrame(wx.Frame):

    def __init__(self, parent):
        # 150
        super(MenuFrame, self).__init__(parent, size=(300, 150))
        self._parent = parent
        self._createSettingsPopupMenu()
        self._initLayout()

    def _initLayout(self):
        self.SetBackgroundColour(wx.WHITE)
        self.SetWindowStyle(wx.FRAME_TOOL_WINDOW)

        windowWidth, windowHeight = self.GetSize()

        topPanelHeight = windowHeight * 0.35
        self.topPanel = self._initLayoutTopPanel(windowWidth, topPanelHeight)

        bottomPanelHeight = windowHeight * 0.22
        self.bottomPanel = self._initLayoutBottomPanel(windowWidth, bottomPanelHeight)

        self.contentPanel = self._initContentPanel()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.topPanel)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(self.contentPanel, wx.SizerFlags(1).Center())
        mainSizer.AddStretchSpacer()
        mainSizer.Add(self.bottomPanel)

        self.SetSizer(mainSizer)

    def _initLayoutTopPanel(self, width, height):
        panel = wx.Panel(self, size=(width, height))
        panel.SetBackgroundColour(colors.PRIMARY)

        self.txtOrg = wx.StaticText(panel, -1, '')
        self.txtOrg.SetForegroundColour(wx.WHITE)
        font = wx.Font(wx.FontInfo(10).Bold())
        self.txtOrg.SetFont(font)

        self.txtEmail = wx.StaticText(panel, -1, '')
        self.txtEmail.SetForegroundColour(wx.WHITE)

        bmpFolder = wx.Bitmap(str(icons.FOLDER), wx.BITMAP_TYPE_PNG)
        self.btnFolder = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmpFolder, style=wx.NO_BORDER,
                                         size=(bmpFolder.GetWidth(), bmpFolder.GetHeight()))
        self.btnFolder.SetBackgroundColour(colors.PRIMARY)
        self.btnFolder.SetToolTip('Abrir pasta com Notas Fiscais')
        self.btnFolder.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        bmpSettings = wx.Bitmap(str(icons.SETTINGS), wx.BITMAP_TYPE_PNG)
        self.btnSettings = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmpSettings, style=wx.NO_BORDER,
                                           size=(bmpSettings.GetWidth(), bmpSettings.GetHeight()))
        self.btnSettings.SetBackgroundColour(colors.PRIMARY)
        self.btnSettings.SetToolTip('Configurações')
        self.btnSettings.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.txtUnauthorized = wx.StaticText(panel, -1, 'Entre para começar')
        font = wx.Font(wx.FontInfo(10).Bold())
        self.txtUnauthorized.SetFont(font)
        self.txtUnauthorized.SetForegroundColour(wx.WHITE)

        self.userSizer = wx.BoxSizer(wx.VERTICAL)
        self.userSizer.Add(self.txtOrg)
        self.userSizer.Add(self.txtEmail)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnFolder, wx.SizerFlags(0).Border(wx.RIGHT, 10)),
        btnSizer.Add(self.btnSettings)

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.txtUnauthorized,
                       wx.SizerFlags(1).Align(wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL).Border(wx.ALL, 10))
        panelSizer.Add(self.userSizer,
                       wx.SizerFlags(1).Align(wx.LEFT | wx.ALIGN_CENTER_VERTICAL).Border(wx.ALL, 10))
        panelSizer.Add(btnSizer,
                       wx.SizerFlags(0).Align(wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL).Border(wx.RIGHT, 10))

        panel.SetSizer(panelSizer)
        return panel

    def _initContentPanel(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.WHITE)

        fontStatus = wx.Font(wx.FontInfo(11).FaceName("Calibri Light"))
        bmpCloudCounter = wx.Bitmap(str(icons.SUCCESS), wx.BITMAP_TYPE_PNG)
        self.bmpCloudCounter = wx.StaticBitmap(panel, -1, bmpCloudCounter, (10, 5),
                                               (bmpCloudCounter.GetWidth(), bmpCloudCounter.GetHeight()))
        self.txtCloudCounter = wx.StaticText(panel, -1, '')
        self.txtCloudCounter.SetFont(fontStatus)
        self.txtCloudCounter.SetToolTip('Notas Fiscais sincronizadas com sucesso')
        self.bmpCloudCounter.SetToolTip('Notas Fiscais sincronizadas com sucesso')

        bmpBlacklistedCounter = wx.Bitmap(str(icons.FAILURE), wx.BITMAP_TYPE_PNG)
        self.bmpBlacklistedCounter = wx.StaticBitmap(panel, -1, bmpBlacklistedCounter, (10, 5),
                                                     (bmpBlacklistedCounter.GetWidth(),
                                                      bmpBlacklistedCounter.GetHeight()))
        self.bmpBlacklistedCounter.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.txtBlacklistedCounter = wx.StaticText(panel, -1, '')
        self.txtBlacklistedCounter.SetFont(fontStatus)
        self.txtBlacklistedCounter.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.txtBlacklistedCounter.SetToolTip('Notas Fiscais com falha de sincronização')
        self.bmpBlacklistedCounter.SetToolTip('Notas Fiscais com falha de sincronização')

        cloudSizer = wx.BoxSizer(wx.HORIZONTAL)
        cloudSizer.Add(self.bmpCloudCounter)
        cloudSizer.Add(self.txtCloudCounter, wx.SizerFlags(0).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 5))

        blacklistedSizer = wx.BoxSizer(wx.HORIZONTAL)
        blacklistedSizer.Add(self.bmpBlacklistedCounter)
        blacklistedSizer.Add(self.txtBlacklistedCounter, wx.SizerFlags(
            0).Expand().Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 5))

        self.countersSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.countersSizer.Add(cloudSizer, wx.SizerFlags(0).Expand().Border(wx.RIGHT, 20))
        self.countersSizer.Add(blacklistedSizer, wx.SizerFlags(0).Expand().Border(wx.LEFT, 20))

        self.btnSignin = widgets.PrimaryButton(panel, 'Entrar')

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.countersSizer, wx.SizerFlags(0).Align(wx.ALIGN_CENTER_VERTICAL | wx.RIGHT))
        panelSizer.Add(self.btnSignin, wx.SizerFlags(0).Align(wx.ALIGN_CENTER_VERTICAL))

        panel.SetSizer(panelSizer)
        return panel

    def _initLayoutBottomPanel(self, width, height):
        panel = wx.Panel(self, size=(width, height))
        panel.SetBackgroundColour(colors.GREY_LIGHT)

        self.txtStatus = wx.StaticText(panel, -1, '', style=wx.ALIGN_RIGHT | wx.ST_NO_AUTORESIZE)
        font = wx.Font(wx.FontInfo(10))
        self.txtStatus.SetFont(font)

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.txtStatus, wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.ALL, 7))

        panel.SetSizer(panelSizer)
        return panel

    def _createSettingsPopupMenu(self):
        self.settingsPopupMenu = wx.Menu()
        self.menuItemSettings = self.settingsPopupMenu.Append(-1, 'Preferências...')
        self.settingsPopupMenu.AppendSeparator()
        self.menuItemExit = self.settingsPopupMenu.Append(wx.ID_EXIT, 'Sair')

    def destroy(self):
        wx.CallAfter(self._parent.Destroy)

    def alignToBottomRight(self):
        _, _, _, dh = wx.ClientDisplayRect()
        position = wx.GetMousePosition()

        w, h = self.GetSize()
        x = position[0] - (w / 2)
        y = dh - h
        self.SetPosition((x, y))

    def start(self):
        self.alignToBottomRight()
        self.Raise()
        self.Show()


class MenuPresenter:

    def __init__(self, view, interactor, menuHandler, syncDataModel, authService, syncManager):
        self._view = view
        interactor.Install(self, self._view)
        self._menuHandler = menuHandler
        self._syncManager = syncManager
        self._syncDataModel = syncDataModel
        self._authService = authService
        self.initView()

    def initView(self):
        self._state = State.UNINITIALIZED
        self._userOrg = ''
        self._userEmail = ''
        self._cloudCounter = 0
        self._blacklistedCounter = 0
        self._loadViewFromModel()

    def updateState(self, state):
        self._state = state
        self.updateModel()

    def updateModel(self):
        syncData = self._syncDataModel.getSyncData()
        self._userOrg = syncData.userOrg
        self._userEmail = syncData.userEmail
        self._lastSync = syncData.lastSync
        self._updateCounters()
        self._loadViewFromModel()

    def _updateCounters(self):
        if self._syncManager.isRunning():
            self._cloudCounter = self._syncManager.cloudFolder.getTotalFiles()
            self._blacklistedCounter = self._syncManager.localFolder.blacklistedFolder.getTotalFiles()
        else:
            self._cloudCounter = 0
            self._blacklistedCounter = 0

    def _loadViewFromModel(self):
        self._view.txtOrg.SetLabel(self._userOrg)
        self._view.txtEmail.SetLabel(self._userEmail)
        self._view.txtCloudCounter.SetLabel(str(self._cloudCounter))
        self._view.txtBlacklistedCounter.SetLabel(str(self._blacklistedCounter))
        self._refreshStatus()
        self._refreshVisibility()
        self._refreshIcons()

        self._view.Layout()
        self._view.Refresh()

    def _refreshStatus(self):
        if self._state == State.UNINITIALIZED or not self._authService.isAuthenticated():
            self._view.txtStatus.SetLabel('Não inicializado')
        if self._state == State.NO_CONNECTION:
            self._view.txtStatus.SetLabel('Desconectado')
        elif self._state == State.SYNCING:
            self._view.txtStatus.SetLabel('Sincronizando...')
        elif self._state == State.IDLE:
            statusLabel = 'Atualizado'
            if self._lastSync:
                delta = datetime.now() - self._lastSync
                statusLabel = f'{ statusLabel } { DeltaTime.format(delta) }'
            self._view.txtStatus.SetLabel(statusLabel)

    def _refreshVisibility(self):
        if self._state == State.UNINITIALIZED or not self._authService.isAuthenticated():
            self._view.userSizer.ShowItems(False)
            self._view.countersSizer.ShowItems(False)
            self._view.btnSignin.Show()
            self._view.txtUnauthorized.Show()
        else:
            self._view.userSizer.ShowItems(True)
            self._view.countersSizer.ShowItems(True)
            self._view.btnSignin.Hide()
            self._view.txtUnauthorized.Hide()

    def _refreshIcons(self):
        bmpCloudCounter = wx.Bitmap(icons.SUCCESS.as_posix(), wx.BITMAP_TYPE_PNG)
        bmpBlacklistedCounter = wx.Bitmap(icons.FAILURE.as_posix(), wx.BITMAP_TYPE_PNG)

        if self._state == State.NO_CONNECTION:
            bmpCloudCounter = wx.Bitmap(icons.SUCCESS_GRAYSCALE.as_posix(), wx.BITMAP_TYPE_PNG)
            bmpBlacklistedCounter = wx.Bitmap(icons.FAILURE_GRAYSCALE.as_posix(), wx.BITMAP_TYPE_PNG)

        self._view.bmpCloudCounter.SetBitmap(bmpCloudCounter)
        self._view.bmpBlacklistedCounter.SetBitmap(bmpBlacklistedCounter)

    def openSyncFolder(self):
        nfsDir = self._syncDataModel.getSyncData().nfsDir
        if nfsDir:
            os.system('start {}'.format(nfsDir))

    def showSettingsPopupMenu(self):
        self._view.btnSettings.PopupMenu(self._view.settingsPopupMenu)

    def showBlacklist(self):
        blacklist.show(self._view, self._syncManager.localFolder.blacklistedFolder)

    def signin(self):
        self._menuHandler.onSignin()

    def showConfig(self):
        self._menuHandler.onConfig()

    def hideView(self):
        self._view.Hide()

    def handleActivate(self, evt):
        if self._view:
            if not evt.GetActive():
                self.hideView()
            else:
                self.updateModel()

    def show(self):
        self._view.start()

    def quit(self):
        self._menuHandler.onExit()


class MenuInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUp)
        self._view.Bind(wx.EVT_ACTIVATE, self.OnActivate)
        self._view.btnFolder.Bind(wx.EVT_BUTTON, self.OnClickFolder)
        self._view.btnSettings.Bind(wx.EVT_BUTTON, self.OnClickSettingsPopupMenu)
        self._view.btnSignin.Bind(wx.EVT_BUTTON, self.OnClickSignin)
        self._view.bmpBlacklistedCounter.Bind(wx.EVT_LEFT_DOWN, self.OnClickBlacklisedCounter)
        self._view.txtBlacklistedCounter.Bind(wx.EVT_LEFT_DOWN, self.OnClickBlacklisedCounter)
        self._view.settingsPopupMenu.Bind(wx.EVT_MENU, self.OnExit, self._view.menuItemExit)
        self._view.settingsPopupMenu.Bind(wx.EVT_MENU, self.OnConfig, self._view.menuItemSettings)

    def OnClickFolder(self, evt):
        self._presenter.openSyncFolder()

    def OnClickBlacklisedCounter(self, evt):
        self._presenter.showBlacklist()

    def OnClickSettingsPopupMenu(self, evt):
        self._presenter.showSettingsPopupMenu()

    def OnClickSignin(self, evt):
        self._presenter.signin()

    def OnConfig(self, evt):
        self._presenter.showConfig()

    def OnActivate(self, evt):
        self._presenter.handleActivate(evt)

    def OnExit(self, evt):
        self._presenter.quit()

    def OnKeyUp(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self._presenter.hideView()
