import wx
import os

from ui import settings
from ui.assets import icons
from quantisync.core.sync import State
from quantisync.core.settings import SettingsSerializer


def create(parent, cloudFolder, blacklistedFolder):
    return MenuPresenter(MenuFrame(parent),
                         MenuInteractor(),
                         SettingsSerializer(),
                         cloudFolder,
                         blacklistedFolder)


class MenuFrame(wx.Frame):

    def __init__(self, parent, title='QuantiSync'):
        super(MenuFrame, self).__init__(parent, title=title, size=(300, 130))
        self._initLayout()

    def _initLayout(self):
        self.SetBackgroundColour("white")
        self.SetWindowStyle(wx.FRAME_TOOL_WINDOW)

        topPanel = self._initLayoutTopPanel()
        contentPanel = self._initContentPanel()
        bottomPanel = self._initLayoutBottomPanel()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topPanel)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(contentPanel, wx.SizerFlags(1).Center())
        mainSizer.AddStretchSpacer()
        mainSizer.Add(bottomPanel)

        self.SetSizer(mainSizer)

    def _initLayoutTopPanel(self):
        frameWidth = self.GetSize()[0]
        panel = wx.Panel(self, size=(frameWidth, 55))
        panel.SetBackgroundColour("#7159C1")

        txtOrganization = wx.StaticText(panel, -1, 'Fonseca LTDA')
        txtOrganization.SetForegroundColour('white')
        font = wx.Font(wx.FontInfo(10).Bold())
        txtOrganization.SetFont(font)

        txtEmail = wx.StaticText(panel, -1, 'gustavofonseca94@gmail.com')
        txtEmail.SetForegroundColour('white')

        bmpFolder = wx.Bitmap(str(icons.FOLDER), wx.BITMAP_TYPE_PNG)
        self.btnFolder = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmpFolder, style=wx.NO_BORDER,
                                         size=(bmpFolder.GetWidth(), bmpFolder.GetHeight()))
        self.btnFolder.SetBackgroundColour('#7159C1')
        self.btnFolder.SetToolTip('Abrir pasta com Notas Fiscais')

        bmpSettings = wx.Bitmap(str(icons.SETTINGS), wx.BITMAP_TYPE_PNG)
        self.btnSettings = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmpSettings, style=wx.NO_BORDER,
                                           size=(bmpSettings.GetWidth(), bmpSettings.GetHeight()))
        self.btnSettings.SetBackgroundColour('#7159C1')
        self.btnSettings.SetToolTip('Configurações')

        userSizer = wx.BoxSizer(wx.VERTICAL)
        userSizer.Add(txtOrganization)
        userSizer.Add(txtEmail)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnFolder, wx.SizerFlags(0).Border(wx.RIGHT, 15)),
        btnSizer.Add(self.btnSettings)

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
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

        bpmFailure = wx.Bitmap(str(icons.FAILURE), wx.BITMAP_TYPE_PNG)
        self.stcBpmFailure = wx.StaticBitmap(panel, -1, bpmFailure, (10, 5),
                                             (bpmFailure.GetWidth(), bpmFailure.GetHeight()))
        self.txtFailure = wx.StaticText(panel, -1, '')
        self.txtFailure.SetFont(fontStatus)

        successSizer = wx.BoxSizer(wx.HORIZONTAL)
        successSizer.Add(self.stcBpmSuccess)
        successSizer.Add(self.txtSuccess, wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 5))

        failureSizer = wx.BoxSizer(wx.HORIZONTAL)
        failureSizer.Add(self.stcBpmFailure)
        failureSizer.Add(self.txtFailure, wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 5))

        statusSizer = wx.BoxSizer(wx.HORIZONTAL)
        statusSizer.Add(successSizer, wx.SizerFlags(0).Border(wx.RIGHT, 20))
        statusSizer.Add(failureSizer, wx.SizerFlags(0).Border(wx.LEFT, 20))

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(statusSizer, wx.SizerFlags(0).Align(wx.ALIGN_CENTER_VERTICAL | wx.RIGHT))

        panel.SetSizer(panelSizer)
        return panel

    def _initLayoutBottomPanel(self):
        frameWidth = self.GetSize()[0]
        panel = wx.Panel(self, size=(frameWidth, 27))
        panel.SetBackgroundColour("#e6eaed")

        self.txtStatus = wx.StaticText(panel, -1, '', style=wx.ALIGN_RIGHT | wx.ST_NO_AUTORESIZE)
        font = wx.Font(wx.FontInfo(10))
        self.txtStatus.SetFont(font)

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self.txtStatus, wx.SizerFlags(1).Border(wx.ALL, 7))

        panel.SetSizer(panelSizer)
        return panel

    def setStatus(self, status):
        self.txtStatus.SetLabel(status)

    def setSuccessfulCounter(self, count):
        self.txtSuccess.SetLabel(str(count))

    def setFailureCounter(self, count):
        self.txtFailure.SetLabel(str(count))

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

    def start(self):
        alignToBottomRight(self)
        self.Raise()
        self.Show()

    def quit(self):
        self.Destroy()


class MenuPresenter:

    def __init__(self, view, interactor, settingsSerializer, cloudFolder, blacklistedFolder):
        self._view = view
        interactor.Install(self, self._view)
        self._cloudFolder = cloudFolder
        self._blacklistedFolder = blacklistedFolder
        self._settingsSerializer = settingsSerializer
        self.initView()

    def initView(self):
        self._status = 'Atualizado'
        self._offline = False
        self._refreshCounters()
        self._loadViewFromModel()

    def show(self):
        self._view.start()

    def _loadViewFromModel(self):
        self._view.setStatus(self._status)
        self._view.setSuccessfulCounter(self._success)
        self._view.setFailureCounter(self._failure)

        if self._offline:
            self._view.setOfflineIcons()
        else:
            self._view.setOnlineIcons()

    def updateModel(self, state):
        if (state == State.SYNCING):
            self._status = 'Sincronizando...'
            self._offline = False
        elif (state == State.NORMAL):
            self._status = 'Atualizado'
            self._offline = False
        elif (state == State.NO_CONNECTION):
            self._status = 'Desconectado'
            self._offline = True
        elif (state == State.UNAUTHORIZED):
            self._status = 'Desconectado'
            self._offline = True

        self._refreshCounters()
        self._loadViewFromModel()

    def _refreshCounters(self):
        self._success = self._cloudFolder.getTotalFiles()
        self._failure = self._blacklistedFolder.getTotalFiles()

    def openSyncFolder(self):
        settings = self._settingsSerializer.load()
        os.system('start {}'.format(settings.nfsDir))

    def showSettings(self):
        settings.show(None)

    def closeIfInactive(self, evt):
        if not evt.GetActive():
            self._view.Hide()


class MenuInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.btnFolder.Bind(wx.EVT_BUTTON, self.OnFolder)
        self._view.btnSettings.Bind(wx.EVT_BUTTON, self.OnSettings)
        self._view.Bind(wx.EVT_ACTIVATE, self.OnActivate)

    def OnFolder(self, evt):
        self._presenter.openSyncFolder()

    def OnSettings(self, evt):
        self._presenter.showSettings()

    def OnActivate(self, evt):
        self._presenter.closeIfInactive(evt)


def alignToBottomRight(frame):
    _, _, _, dh = wx.ClientDisplayRect()
    position = wx.GetMousePosition()

    w, h = frame.GetSize()
    x = position[0] - (w / 2)
    y = dh - h
    frame.SetPosition((x, y))
