import wx
import os
from datetime import datetime

from ui import settings, blacklist, wizard
from ui.app import app
from ui.assets import icons

from quantisync.core.sync import State
from quantisync.lib.util import DeltaTime


def create(parent):
    return MenuPresenter(MenuFrame(parent),
                         MenuInteractor(),
                         app.syncDataModel,
                         app.authService,
                         app.syncManager)


class MenuFrame(wx.Frame):

    def __init__(self, parent, title='QuantiSync'):
        super(MenuFrame, self).__init__(parent, title=title, size=(300, 150))
        self._parent = parent
        self._createSettingsPopupMenu()
        self._initLayout()

    def _initLayout(self):
        self.SetBackgroundColour("white")
        self.SetWindowStyle(wx.FRAME_TOOL_WINDOW)

        self.topPanel = self._initLayoutTopPanel()
        self.contentPanel = self._initContentPanel()
        self.bottomPanel = self._initLayoutBottomPanel()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.topPanel)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(self.contentPanel, wx.SizerFlags(1).Center())
        mainSizer.AddStretchSpacer()
        mainSizer.Add(self.bottomPanel)

        self.SetSizer(mainSizer)

    def _initLayoutTopPanel(self):
        frameWidth = self.GetSize()[0]
        panel = wx.Panel(self, size=(frameWidth, 55))
        panel.SetBackgroundColour("#7159C1")

        self.txtOrg = wx.StaticText(panel, -1, '')
        self.txtOrg.SetForegroundColour('white')
        font = wx.Font(wx.FontInfo(10).Bold())
        self.txtOrg.SetFont(font)

        self.txtEmail = wx.StaticText(panel, -1, '')
        self.txtEmail.SetForegroundColour('white')

        bmpFolder = wx.Bitmap(str(icons.FOLDER), wx.BITMAP_TYPE_PNG)
        self.btnFolder = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmpFolder, style=wx.NO_BORDER,
                                         size=(bmpFolder.GetWidth(), bmpFolder.GetHeight()))
        self.btnFolder.SetBackgroundColour('#7159C1')
        self.btnFolder.SetToolTip('Abrir pasta com Notas Fiscais')
        self.btnFolder.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        bmpSettings = wx.Bitmap(str(icons.SETTINGS), wx.BITMAP_TYPE_PNG)
        self.btnSettings = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmpSettings, style=wx.NO_BORDER,
                                           size=(bmpSettings.GetWidth(), bmpSettings.GetHeight()))
        self.btnSettings.SetBackgroundColour('#7159C1')
        self.btnSettings.SetToolTip('Configurações')
        self.btnSettings.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.txtUnauthorized = wx.StaticText(panel, -1, 'Entre para começar')
        font = wx.Font(wx.FontInfo(10).Bold())
        self.txtUnauthorized.SetFont(font)
        self.txtUnauthorized.SetForegroundColour('white')

        userSizer = wx.BoxSizer(wx.VERTICAL)
        userSizer.Add(self.txtOrg)
        userSizer.Add(self.txtEmail)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnFolder, wx.SizerFlags(0).Border(wx.RIGHT, 10)),
        btnSizer.Add(self.btnSettings)

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.txtUnauthorized, wx.SizerFlags(1).Align(
            wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL).Border(wx.ALL, 10))
        panelSizer.Add(userSizer, wx.SizerFlags(1).Left().Border(wx.ALL, 10))
        panelSizer.Add(btnSizer, wx.SizerFlags(0).Align(
            wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL).Border(wx.RIGHT, 10))

        panel.SetSizer(panelSizer)
        return panel

    def _initContentPanel(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour("white")

        fontStatus = wx.Font(wx.FontInfo(11).FaceName("Calibri Light"))
        bpmSuccess = wx.Bitmap(str(icons.SUCCESS), wx.BITMAP_TYPE_PNG)
        self.stcBpmSuccess = wx.StaticBitmap(panel, -1, bpmSuccess, (10, 5),
                                             (bpmSuccess.GetWidth(), bpmSuccess.GetHeight()))
        self.txtSuccess = wx.StaticText(panel, -1, '')
        self.txtSuccess.SetFont(fontStatus)
        self.setSuccessfulCounterTooltip('Notas Fiscais sincronizadas com sucesso')

        bpmFailure = wx.Bitmap(str(icons.FAILURE), wx.BITMAP_TYPE_PNG)
        self.stcBpmFailure = wx.StaticBitmap(panel, -1, bpmFailure, (10, 5),
                                             (bpmFailure.GetWidth(), bpmFailure.GetHeight()))
        self.stcBpmFailure.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.txtFailure = wx.StaticText(panel, -1, '')
        self.txtFailure.SetFont(fontStatus)
        self.txtFailure.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.setFailureCounterTooltip('Notas Fiscais com falha de sincronização')

        successSizer = wx.BoxSizer(wx.HORIZONTAL)
        successSizer.Add(self.stcBpmSuccess)
        successSizer.Add(self.txtSuccess, wx.SizerFlags(0).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 5))

        failureSizer = wx.BoxSizer(wx.HORIZONTAL)
        failureSizer.Add(self.stcBpmFailure)
        failureSizer.Add(self.txtFailure, wx.SizerFlags(0).Expand().Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 5))

        statusSizer = wx.BoxSizer(wx.HORIZONTAL)
        statusSizer.Add(successSizer, wx.SizerFlags(0).Expand().Border(wx.RIGHT, 20))
        statusSizer.Add(failureSizer, wx.SizerFlags(0).Expand().Border(wx.LEFT, 20))

        self.btnSignin = wx.Button(panel, label='Entrar', size=(80, 26), style=wx.BORDER_NONE)
        self.btnSignin.SetBackgroundColour("#7159C1")
        self.btnSignin.SetForegroundColour('white')

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(statusSizer, wx.SizerFlags(0).Align(wx.ALIGN_CENTER_VERTICAL | wx.RIGHT))
        panelSizer.Add(self.btnSignin, wx.SizerFlags(0).Align(wx.ALIGN_CENTER_VERTICAL))

        panel.SetSizer(panelSizer)
        return panel

    def _initLayoutBottomPanel(self):
        frameWidth = self.GetSize()[0]
        panel = wx.Panel(self, size=(frameWidth, 30))
        panel.SetBackgroundColour("#e6eaed")

        self.txtStatus = wx.StaticText(panel, -1, '', style=wx.ALIGN_RIGHT | wx.ST_NO_AUTORESIZE)
        font = wx.Font(wx.FontInfo(10))
        self.txtStatus.SetFont(font)

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.txtStatus, wx.SizerFlags(1).Border(wx.ALL, 7))

        panel.SetSizer(panelSizer)
        return panel

    def _createSettingsPopupMenu(self):
        self.settingsPopupMenu = wx.Menu()
        self.menuItemSettings = self.settingsPopupMenu.Append(-1, 'Configurações')
        self.settingsPopupMenu.AppendSeparator()
        self.menuItemExit = self.settingsPopupMenu.Append(wx.ID_EXIT, 'Sair')

    def showSettingsPopupMenu(self):
        self.btnSettings.PopupMenu(self.settingsPopupMenu)

    def setUser(self, userOrg, userEmail):
        self.txtOrg.SetLabel(userOrg)
        self.txtEmail.SetLabel(userEmail)

    def setStatus(self, status):
        self.txtStatus.SetLabel(status)

    def setSuccessfulCounter(self, count):
        self.txtSuccess.SetLabel(str(count))
        self.Layout()

    def setSuccessfulCounterTooltip(self, tooltip):
        self.txtSuccess.SetToolTip(tooltip)
        self.stcBpmSuccess.SetToolTip(tooltip)

    def setFailureCounter(self, count):
        self.txtFailure.SetLabel(str(count))
        self.Layout()

    def setFailureCounterTooltip(self, tooltip):
        self.txtFailure.SetToolTip(tooltip)
        self.stcBpmFailure.SetToolTip(tooltip)

    def setUnauthorized(self):
        self.txtOrg.Hide()
        self.txtEmail.Hide()
        self.txtFailure.Hide()
        self.txtSuccess.Hide()
        self.stcBpmFailure.Hide()
        self.stcBpmSuccess.Hide()
        self.btnSignin.Show()
        self.txtUnauthorized.Show()
        self.Layout()

    def setAuthorized(self):
        self.txtOrg.Show()
        self.txtEmail.Show()
        self.txtFailure.Show()
        self.txtSuccess.Show()
        self.stcBpmFailure.Show()
        self.stcBpmSuccess.Show()
        self.btnSignin.Hide()
        self.txtUnauthorized.Hide()
        self.Layout()

    def setOfflineIcons(self):
        bpmSuccess = wx.Bitmap(str(icons.SUCCESS_GRAYSCALE), wx.BITMAP_TYPE_PNG)
        self.stcBpmSuccess.SetBitmap(bpmSuccess)
        bpmFailure = wx.Bitmap(str(icons.FAILURE_GRAYSCALE), wx.BITMAP_TYPE_PNG)
        self.stcBpmFailure.SetBitmap(bpmFailure)

    def setOnlineIcons(self):
        bpmSuccess = wx.Bitmap(str(icons.SUCCESS), wx.BITMAP_TYPE_PNG)
        self.stcBpmSuccess.SetBitmap(bpmSuccess)
        bpmFailure = wx.Bitmap(str(icons.FAILURE), wx.BITMAP_TYPE_PNG)
        self.stcBpmFailure.SetBitmap(bpmFailure)

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

    def __init__(self, view, interactor, syncDataModel, authService, syncManager):
        self._view = view
        interactor.Install(self, self._view)
        self._syncManager = syncManager
        self._syncDataModel = syncDataModel
        self._authService = authService
        self.initView()

    def initView(self):
        self._state = State.NORMAL
        self.updateModel()

    def show(self):
        self._view.start()

    def updateState(self, state):
        self._state = state
        self.updateModel()

    def updateModel(self):
        self._syncData = self._syncDataModel.getSyncData()
        self._refreshStatus()
        self._refreshCounters()
        self._loadViewFromModel()

    def _loadViewFromModel(self):
        self._view.setUser(self._syncData.userOrg, self._syncData.userEmail)
        self._view.setStatus(self._status)
        self._view.setSuccessfulCounter(self._success)
        self._view.setFailureCounter(self._failure)

        if (self._state == State.UNAUTHORIZED or not self._authService.isAuthenticated()):
            self._view.setUnauthorized()
        else:
            self._view.setAuthorized()

        if (self._state == State.NO_CONNECTION):
            self._view.setOfflineIcons()
        else:
            self._view.setOnlineIcons()

    def _refreshCounters(self):
        if self._syncManager.isRunning():
            self._success = self._syncManager.cloudFolder.getTotalFiles()
            self._failure = self._syncManager.localFolder.blacklistedFolder.getTotalFiles()
        else:
            self._success = 0
            self._failure = 0

    def _refreshStatus(self):
        if (self._state == State.NO_CONNECTION):
            self.updateNoConnectionStatus()
        elif (self._state == State.UNAUTHORIZED or not self._authService.isAuthenticated()):
            self.updateUnauthorizedStatus()
        elif (self._state == State.SYNCING):
            self.updateSyncingStatus()
        elif (self._state == State.NORMAL):
            self.updateNormalStatus()

    def updateSyncingStatus(self):
        self._status = 'Sincronizando...'

    def updateNormalStatus(self):
        self._status = 'Atualizado'
        if self._syncData.lastSync:
            delta = datetime.now() - self._syncData.lastSync
            self._status = self._status + ' ' + DeltaTime.format(delta)

    def updateUnauthorizedStatus(self):
        self._status = 'Não autenticado'

    def updateNoConnectionStatus(self):
        self._status = 'Desconectado'

    def openSyncFolder(self):
        os.system('start {}'.format(self._syncData.nfsDir))

    def showSettingsPopupMenu(self):
        self._view.showSettingsPopupMenu()

    def showSettings(self):
        settings.show(self._view)

    def showBlacklist(self):
        blacklist.show(self._view, self._syncManager.localFolder.blacklistedFolder)

    def signin(self):
        wizard.show(self._view._parent)

    def hideView(self):
        self._view.Hide()

    def handleActivate(self, evt):
        if self._view:
            if not evt.GetActive():
                self.hideView()
            else:
                self.updateModel()

    def destroy(self):
        self._view.destroy()


class MenuInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUp)
        self._view.Bind(wx.EVT_ACTIVATE, self.OnActivate)
        self._view.btnFolder.Bind(wx.EVT_BUTTON, self.OnClickFolder)
        self._view.btnSettings.Bind(wx.EVT_BUTTON, self.OnClickSettingsPopupMenu)
        self._view.btnSignin.Bind(wx.EVT_BUTTON, self.OnClickSignin)
        self._view.stcBpmFailure.Bind(wx.EVT_LEFT_DOWN, self.OnClickFailureCounter)
        self._view.txtFailure.Bind(wx.EVT_LEFT_DOWN, self.OnClickFailureCounter)
        self._view.settingsPopupMenu.Bind(wx.EVT_MENU, self.OnExit, self._view.menuItemExit)
        self._view.settingsPopupMenu.Bind(wx.EVT_MENU, self.OnSettings, self._view.menuItemSettings)

    def OnClickFolder(self, evt):
        self._presenter.openSyncFolder()

    def OnClickFailureCounter(self, evt):
        self._presenter.showBlacklist()

    def OnClickSettingsPopupMenu(self, evt):
        self._presenter.showSettingsPopupMenu()

    def OnClickSignin(self, evt):
        self._presenter.signin()

    def OnSettings(self, evt):
        self._presenter.showSettings()

    def OnActivate(self, evt):
        self._presenter.handleActivate(evt)

    def OnExit(self, evt):
        self._presenter.destroy()

    def OnKeyUp(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self._presenter.hideView()
