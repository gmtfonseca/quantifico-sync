import wx

from ui.assets import icons


def show(parent):
    return MenuPresenter(MenuFrame(parent),
                         MenuInteractor())


class MenuFrame(wx.Frame):

    def __init__(self, parent, title='QuantiSync'):
        super(MenuFrame, self).__init__(parent, title=title, size=(310, 125))
        self._initLayout()

    def _initLayout(self):
        self.SetBackgroundColour("white")

        topPanel = self._initLayoutTopPanel()
        contentPanel = self._initContentPanel()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topPanel)
        mainSizer.Add(contentPanel, wx.SizerFlags(1).Center())

        self.SetSizer(mainSizer)

    def _initLayoutTopPanel(self):
        topPanel = wx.Panel(self, size=(310, 55))
        topPanel.SetBackgroundColour("#7159C1")

        txtOrganization = wx.StaticText(topPanel, -1, 'Fonseca LTDA')
        txtOrganization.SetForegroundColour('white')
        font = wx.Font(wx.FontInfo(10).Bold())
        txtOrganization.SetFont(font)

        txtEmail = wx.StaticText(topPanel, -1, 'gustavofonseca94@gmail.com')
        txtEmail.SetForegroundColour('white')

        bmpFolder = wx.Bitmap(str(icons.FOLDER), wx.BITMAP_TYPE_PNG)
        btnFolder = wx.BitmapButton(topPanel, id=wx.ID_ANY, bitmap=bmpFolder, style=wx.NO_BORDER,
                                    size=(bmpFolder.GetWidth(), bmpFolder.GetHeight()))
        btnFolder.SetBackgroundColour('#7159C1')
        btnFolder.SetToolTip('Abrir pasta com Notas Fiscais')

        bmpSettings = wx.Bitmap(str(icons.SETTINGS), wx.BITMAP_TYPE_PNG)
        btnSettings = wx.BitmapButton(topPanel, id=wx.ID_ANY, bitmap=bmpSettings, style=wx.NO_BORDER,
                                      size=(bmpSettings.GetWidth(), bmpSettings.GetHeight()))
        btnSettings.SetBackgroundColour('#7159C1')
        btnSettings.SetToolTip('Configurações')

        userSizer = wx.BoxSizer(wx.VERTICAL)
        userSizer.Add(txtOrganization)
        userSizer.Add(txtEmail)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(btnFolder, wx.SizerFlags(0).Border(wx.RIGHT, 15))
        btnSizer.Add(btnSettings)

        topPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        topPanelSizer.Add(userSizer, wx.SizerFlags(1).Left().Border(wx.ALL, 10))
        topPanelSizer.Add(btnSizer, wx.SizerFlags(0).Align(
            wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL).Border(wx.RIGHT, 10))

        topPanel.SetSizer(topPanelSizer)
        return topPanel

    def _initContentPanel(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour("white")

        font = wx.Font(wx.FontInfo(13).FaceName("Calibri Light"))

        bpmSuccess = wx.Bitmap(str(icons.SUCCESS), wx.BITMAP_TYPE_PNG)
        stcBpmSuccess = wx.StaticBitmap(panel, -1, bpmSuccess, (10, 5), (bpmSuccess.GetWidth(), bpmSuccess.GetHeight()))
        txtSuccess = wx.StaticText(panel, -1, '3025')
        txtSuccess.SetFont(font)

        bpmFailure = wx.Bitmap(str(icons.FAILURE), wx.BITMAP_TYPE_PNG)
        stcBpmFailure = wx.StaticBitmap(panel, -1, bpmFailure, (10, 5), (bpmFailure.GetWidth(), bpmFailure.GetHeight()))
        txtFailure = wx.StaticText(panel, -1, '7')
        txtFailure.SetFont(font)

        successSizer = wx.BoxSizer(wx.HORIZONTAL)
        successSizer.Add(stcBpmSuccess)
        successSizer.Add(txtSuccess, wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 5))

        failureSizer = wx.BoxSizer(wx.HORIZONTAL)
        failureSizer.Add(stcBpmFailure)
        failureSizer.Add(txtFailure, wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 5))

        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(successSizer, wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.RIGHT, 20))
        panelSizer.Add(failureSizer, wx.SizerFlags(1).Align(wx.ALIGN_CENTER_VERTICAL).Border(wx.LEFT, 20))

        panel.SetSizer(panelSizer)
        return panel

    def start(self):
        alignToBottomRight(self)
        self.SetWindowStyle(wx.FRAME_TOOL_WINDOW)
        self.Raise()
        self.Show()

    def IsShownOnScreen(self):
        return self.IsShownOnScreen()

    def quit(self):
        self.Destroy()


class MenuPresenter:

    def __init__(self, view, interactor):
        self._view = view
        interactor.Install(self, self._view)
        self._initView()
        self._view.start()

    def _initView(self):
        self._loadViewFromModel()

    def _loadViewFromModel(self):
        pass

    def updateModel(self):
        pass

    def closeIfInactive(self, evt):
        if not evt.GetActive():
            self._view.Destroy()


class MenuInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(wx.EVT_ACTIVATE, self.OnActivate)

    def OnOk(self, evt):
        self._presenter.updateModel()

    def OnActivate(self, evt):
        self._presenter.closeIfInactive(evt)


def alignToBottomRight(frame):
    _, _, _, dh = wx.ClientDisplayRect()
    position = wx.GetMousePosition()

    w, h = frame.GetSize()
    x = position[0] - (w / 2)
    y = dh - h
    frame.SetPosition((x, y))
