import wx

from ui.assets import icons, images
# from ui.app import app


def show(parent):
    icon = wx.Icon(str(icons.CLOUD))
    return WizardPresenter(WizardFrame(parent, icon),
                           WizardInteractor())


class WizardFrame(wx.Frame):

    def __init__(self, parent, icon, title='Bem-vindo ao Quantifico (Etapa 1 de 2)'):
        super(WizardFrame, self).__init__(title=title, parent=parent, size=(800, 600))
        self._initLayout()
        self.SetIcon(icon)

    def _initLayout(self):
        self.SetBackgroundColour("white")
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.leftPanel = self._initLeftPanel()
        self.rightPanel = self._initRightPanel()
        mainSizer.Add(self.leftPanel)
        mainSizer.Add(self.rightPanel)

        self.SetSizer(mainSizer)
        # mainSizer.Fit(self)

    def _initLeftPanel(self):
        panel = wx.Panel(self, style=wx.SUNKEN_BORDER, size=(220, 600))
        panel.SetBackgroundColour('#fbfcfe')

        # AUTH PANEL
        authStepBox = wx.Panel(panel, style=wx.NO_BORDER, size=(220, 60))
        authStepBox.SetBackgroundColour('#f0f2f5')
        # authStepPanel.SetBackgroundColour('edf1fb')

        onePng = wx.Image(str(icons.FIRST), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        oneBmp = wx.StaticBitmap(authStepBox, -1, onePng,  size=(onePng.GetWidth(), onePng.GetHeight()))

        txtAuthStep = wx.StaticText(authStepBox, -1, 'Fazer login')
        font = wx.Font(wx.FontInfo(10).Bold())
        txtAuthStep.SetFont(font)
        txtAuthStep.SetForegroundColour('#6c5ce7')

        authStepSizer = wx.BoxSizer(wx.VERTICAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        h2.Add(oneBmp, 0, wx.CENTER)
        h2.Add(txtAuthStep, wx.SizerFlags(0).Center().Border(wx.LEFT, 10))
        authStepSizer.Add(h2, wx.SizerFlags(1).Left().Border(wx.LEFT, 25))

        authStepBox.SetSizer(authStepSizer)

        # FOLDER PANEL
        accountStepPanel = wx.Panel(panel, style=wx.NO_BORDER, size=(220, 60))
        accountStepPanel.SetBackgroundColour('f0f2f5')

        twoPng = wx.Image(str(icons.SECOND), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        twoBpm = wx.StaticBitmap(accountStepPanel, -1, twoPng,  size=(twoPng.GetWidth(), twoPng.GetHeight()))

        txtSync = wx.StaticText(accountStepPanel, -1, 'Parametrização')
        font = wx.Font(wx.FontInfo(10).Bold())
        txtSync.SetFont(font)
        txtSync.SetForegroundColour('black')

        accountStepSizer = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)

        h1.Add(twoBpm, 1, wx.CENTER)
        h1.Add(txtSync, wx.SizerFlags(0).Center().Border(wx.LEFT, 10))

        accountStepSizer.Add(h1, wx.SizerFlags(1).Left().Border(wx.LEFT, 25))
        accountStepPanel.SetSizer(accountStepSizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(authStepBox, wx.SizerFlags(0).Border(wx.TOP, 30))
        sizer.Add(accountStepPanel, wx.SizerFlags(0).Expand())
        panel.SetSizer(sizer)

        return panel

    def _initRightPanel(self):
        panel = wx.Panel(self, size=(580, 600))
        panel.SetBackgroundColour('white')

        title = wx.StaticText(panel, -1, 'Quantifico', (20, 120))
        title.SetForegroundColour('#a29bfe')
        font = wx.Font(wx.FontInfo(25).FaceName("Calibri Light"))
        title.SetFont(font)

        subTitle = wx.StaticText(panel, -1, 'Visualize o seu negócio sem complicações e de qualquer lugar.')
        subTitle.SetForegroundColour('#636e72')
        font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        subTitle.SetFont(font)

        IMG = images.AUTH_BACKGROUND
        png = wx.Image(str(IMG), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        bpm = wx.StaticBitmap(panel, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        self.txtEmail = wx.TextCtrl(panel, size=(250, 25))
        self.txtEmail.SetHint('Insira o seu endereço de email')

        self.txtPassword = wx.TextCtrl(panel, style=wx.TE_PASSWORD, size=(250, 25))
        self.txtPassword.SetHint('Insira a sua senha')

        self.btnSignin = wx.Button(panel, label='Entrar', size=(80, 26), style=wx.BORDER_NONE)
        self.btnSignin.SetBackgroundColour("#6c5ce7")
        self.btnSignin.SetForegroundColour('white')

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnSignin, wx.SizerFlags(0).Border(wx.ALL, 5))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(title, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(subTitle, wx.SizerFlags(0).Center().Border(wx.BOTTOM, 35))
        mainSizer.Add(bpm, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(self.txtEmail, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(self.txtPassword, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(btnSizer, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.AddStretchSpacer()

        panel.SetSizer(mainSizer)

        return panel

    def start(self):
        self.CenterOnScreen()
        self.Raise()
        self.Show()

    def quit(self):
        self.Destroy()


class WizardPresenter:

    def __init__(self, view, interactor):

        self._view = view
        interactor.Install(self, self._view)
        self._initView()
        self._view.start()

    def _initView(self):
        pass

    def _loadViewFromModel(self):
        pass

    def updateModel(self):
        pass


class WizardInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        # self._view.btnOk.Bind(wx.EVT_BUTTON, self.OnOk)

    def OnOk(self, evt):
        self._presenter.updateModel()
