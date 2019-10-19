from threading import Thread

import wx

from quantisync.core.auth import EmptyUser, InvalidUser

from ui.assets import icons, images, colors
from ui.components import widgets


def create(parent, syncDataModel, authService, syncManager, cloudFolder):
    icon = wx.Icon(str(icons.CLOUD))
    return WizardPresenter(WizardFrame(parent, icon),
                           WizardInteractor(),
                           syncDataModel,
                           authService,
                           syncManager,
                           cloudFolder)


class WizardFrame(wx.Frame):

    def __init__(self, parent, icon):
        super(WizardFrame, self).__init__(parent=parent, size=(
            800, 600), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_NO_TASKBAR)
        self._parent = parent
        self._initLayout()
        self.SetIcon(icon)

    def _initLayout(self):
        self.SetBackgroundColour("white")

        self.leftPanel = self._initLeftPanel()
        self.firstStepPanel = self._initFirstStepPanel()
        self.secondStepPanel = self._initSecondStepPanel()

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.leftPanel)
        mainSizer.Add(self.firstStepPanel)
        mainSizer.Add(self.secondStepPanel)
        self.SetSizer(mainSizer)

    def _initLeftPanel(self):
        panel = wx.Panel(self, size=(220, 600))
        panel.SetBackgroundColour(colors.PRIMARY)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(wx.FontInfo(11))

        pngFirstStep = wx.Image(str(icons.ONE), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bmpFirstStep = wx.StaticBitmap(panel, -1, pngFirstStep,
                                            size=(pngFirstStep.GetWidth(), pngFirstStep.GetHeight()))

        txtFirstStep = wx.StaticText(panel, -1, 'Fazer login')
        txtFirstStep.SetFont(font)
        txtFirstStep.SetForegroundColour(wx.WHITE)

        pngSecondStep = wx.Image(str(icons.TWO), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bmpSecondStep = wx.StaticBitmap(panel, -1, pngSecondStep,
                                             size=(pngSecondStep.GetWidth(), pngSecondStep.GetHeight()))

        txtSecondStep = wx.StaticText(panel, -1, 'Configuração')
        txtSecondStep.SetFont(font)
        txtSecondStep.SetForegroundColour(wx.WHITE)

        firstStepSizer = wx.BoxSizer(wx.HORIZONTAL)
        firstStepSizer.Add(self.bmpFirstStep, wx.SizerFlags(0).Center().Border(wx.LEFT, 20))
        firstStepSizer.Add(txtFirstStep, wx.SizerFlags(0).Center().Border(wx.LEFT, 10))

        secondStepSizer = wx.BoxSizer(wx.HORIZONTAL)
        secondStepSizer.Add(self.bmpSecondStep, wx.SizerFlags(0).Center().Border(wx.LEFT, 20))
        secondStepSizer.Add(txtSecondStep, wx.SizerFlags(0).Center().Border(wx.LEFT, 10))

        mainSizer.Add(firstStepSizer, wx.SizerFlags(0).Border(wx.TOP, 30))
        mainSizer.Add(secondStepSizer, wx.SizerFlags(0).Border(wx.TOP, 30))

        panel.SetSizer(mainSizer)

        return panel

    def _initFirstStepPanel(self):
        panel = wx.Panel(self, size=(580, 600))
        panel.SetBackgroundColour(wx.WHITE)

        txtTitle = wx.StaticText(panel, -1, 'Quantifico', (20, 120))
        txtTitle.SetForegroundColour(colors.PRIMARY_LIGHT)
        txtTitleFont = wx.Font(wx.FontInfo(25).FaceName("Calibri Light"))
        txtTitle.SetFont(txtTitleFont)

        txtSubtitle = wx.StaticText(panel, -1, 'Visualize o seu negócio sem complicações e de qualquer lugar.')
        txtSubtitle.SetForegroundColour(colors.GREY)
        txtSubtitleFont = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        txtSubtitle.SetFont(txtSubtitleFont)

        pngBackground = wx.Image(str(images.AUTH_BACKGROUND), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        bmpBackground = wx.StaticBitmap(panel, -1, pngBackground,
                                        size=(pngBackground.GetWidth(), pngBackground.GetHeight()))

        self.txtEmail = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(250, 25))
        self.txtEmail.SetHint('Insira o seu endereço de email')

        self.txtPassword = wx.TextCtrl(panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER, size=(250, 25))
        self.txtPassword.SetHint('Insira a sua senha')

        self.txtStatus = wx.StaticText(
            panel, -1, '')
        self.txtStatus.SetForegroundColour(wx.RED)
        self.txtStatus.Hide()

        aniLoading = wx.adv.Animation(str(images.LOADING))
        self.ctrlLoading = wx.adv.AnimationCtrl(panel, -1, aniLoading)
        self.ctrlLoading.SetBackgroundColour(panel.GetBackgroundColour())
        self.ctrlLoading.Hide()

        self.btnSignin = widgets.PrimaryButton(panel, 'Entrar', size=(250, 30))

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnSignin, wx.SizerFlags(0).Border(wx.ALL, 5))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(txtTitle, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(txtSubtitle, wx.SizerFlags(0).Center().Border(wx.BOTTOM, 35))
        mainSizer.Add(bmpBackground, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(self.txtEmail, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(self.txtPassword, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(self.ctrlLoading, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(self.txtStatus, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.Add(btnSizer, wx.SizerFlags(0).Center().Border(wx.ALL, 5))
        mainSizer.AddStretchSpacer()

        panel.SetSizer(mainSizer)

        return panel

    def _initSecondStepPanel(self):
        panel = wx.Panel(self, size=(580, 600))
        panel.SetBackgroundColour('white')

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, -1, 'Configuração')
        font = wx.Font(wx.FontInfo(13).Bold())
        title.SetFont(font)

        nfsDirFont = wx.Font(wx.FontInfo(10))
        lblNfsDir = wx.StaticText(panel, -1, 'Localização da pasta com as Notas Fiscais:')
        lblNfsDir.SetFont(nfsDirFont)

        self.txtNfsDir = wx.StaticText(panel, -1, '')
        self.txtNfsDir.SetFont(nfsDirFont)
        self.txtNfsDir.SetForegroundColour(colors.GREY)

        self.nfsDir = wx.GenericDirCtrl(panel, -1, size=(-1, 380), style=wx.DIRCTRL_DIR_ONLY)

        self.btnCancel = widgets.SecondaryButton(panel,  'CANCELAR')
        self.btnConfirmNfsDir = widgets.PrimaryButton(panel,  'OK')

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.btnCancel, wx.SizerFlags(0).Border(wx.RIGHT, 10))
        btnSizer.Add(self.btnConfirmNfsDir)

        nfsPathSizer = wx.BoxSizer(wx.HORIZONTAL)
        nfsPathSizer.Add(lblNfsDir, wx.SizerFlags(0))
        nfsPathSizer.Add(self.txtNfsDir, wx.SizerFlags(0).Border(wx.LEFT, 5))

        nfsDirSizer = wx.BoxSizer(wx.HORIZONTAL)
        nfsDirSizer.Add(self.nfsDir, wx.SizerFlags(1).Expand().Border(wx.TOP, 15))

        mainSizer.Add(title, wx.SizerFlags(0).Border(wx.TOP | wx.LEFT, 25))
        mainSizer.Add(nfsPathSizer, wx.SizerFlags(0).Expand().Border(wx.TOP | wx.LEFT, 25))
        mainSizer.Add(nfsDirSizer, wx.SizerFlags(0).Expand().Border(wx.LEFT | wx.RIGHT, 25))
        mainSizer.Add(btnSizer, wx.SizerFlags(0).Right().Border(wx.ALL, 25))

        panel.SetSizer(mainSizer)

        return panel

    def showExistingSnapshotDialog(self):
        dlg = wx.MessageDialog(self, 'Esta conta já possui notas vinculadas, deseja continuar?',
                               'Quantifico', style=wx.YES_NO)
        confirm = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return confirm

    def start(self):
        self.Raise()
        self.Show()

    def destroy(self):
        self.Destroy()


class WizardPresenter:

    def __init__(self, view, interactor, syncDataModel, authService, syncManager, cloudFolder):

        self._view = view
        self._view.CenterOnScreen()
        interactor.Install(self, self._view)
        self._initView()
        self._syncDataModel = syncDataModel
        self._authService = authService
        self._syncManager = syncManager
        self._cloudFolder = cloudFolder
        self._authThread = None

    def _initView(self):
        self._currStep = 1
        self._email = ''
        self._password = ''
        self._statusLabel = ''
        self._nfsDirPath = ''
        self._loadViewFromModel()
        self._setInitialFocus()

    def _loadViewFromModel(self):
        self._view.txtEmail.SetLabel(self._email)
        self._view.txtPassword.SetLabel(self._password)
        self._view.txtNfsDir.SetLabel(self._nfsDirPath)
        self._view.txtStatus.SetLabel(self._statusLabel)
        self._loadCurrStep()
        self._view.Layout()
        self._view.Refresh()

    def _setInitialFocus(self):
        self._view.txtEmail.SetFocus()

    def _loadCurrStep(self):
        if self._currStep == 1:
            self._loadFirstStep()
        elif self._currStep == 2:
            self._loadSecondStep()

    def _loadFirstStep(self):
        self._setTitleStep(1)
        bmpFirstStepFocused = wx.Image(str(icons.ONE_FOCUSED), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._view.bmpFirstStep.SetBitmap(bmpFirstStepFocused)

        bmpSecondStep = wx.Image(str(icons.TWO), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._view.bmpSecondStep.SetBitmap(bmpSecondStep)

        self._view.secondStepPanel.Hide()
        self._view.firstStepPanel.Show()

    def _loadSecondStep(self):
        self._setTitleStep(2)

        bmpFirstStep = wx.Image(str(icons.ONE), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._view.bmpFirstStep.SetBitmap(bmpFirstStep)

        bmpSecondStepFocused = wx.Image(str(icons.TWO_FOCUSED), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._view.bmpSecondStep.SetBitmap(bmpSecondStepFocused)

        self._view.firstStepPanel.Hide()
        self._view.secondStepPanel.Show()

    def _setTitleStep(self, step):
        self._view.SetTitle('Bem-vindo ao Quantifico (Etapa {} de 2)'.format(str(self._currStep)))

    def _nextStep(self):
        self._currStep += 1
        self._loadViewFromModel()

    def setStatusLabel(self, label):
        self._statusLabel = label
        self._loadViewFromModel()

    def updateModel(self):
        self._email = self._view.txtEmail.GetValue()
        self._password = self._view.txtPassword.GetValue()
        self._nfsDirPath = self._view.nfsDir.GetPath()
        self._loadViewFromModel()

    def confirmNfsDir(self):
        self.updateModel()
        self._syncDataModel.setNfsDir(self._nfsDirPath)
        self._startSync()
        self.quit()

    def _startSync(self):
        try:
            self._syncManager.start()
        except Exception as err:
            print(err)
            pass

    def signin(self):
        if not self._authThread or not self._authThread.is_alive():
            self.enableLoading()
            self._authThread = Thread(target=self._requestSignin)
            self._authThread.start()

    def enableLoading(self):
        self._view.txtStatus.Hide()
        self._view.btnSignin.Hide()
        self._view.ctrlLoading.Show()
        self._view.ctrlLoading.Play()
        self._view.Layout()
        self._view.Refresh()

    def disableLoading(self):
        self._view.txtStatus.Show()
        self._view.btnSignin.Show()
        self._view.ctrlLoading.Stop()
        self._view.ctrlLoading.Hide()
        self._view.Layout()
        self._view.Refresh()

    def _requestSignin(self):
        try:
            self.updateModel()
            self._authService.signin(self._email, self._password)
            wx.CallAfter(self._checkExistingSnapshot)
        except EmptyUser:
            self.setStatusLabel('Informe o seu usuário e senha.')
        except InvalidUser:
            self.setStatusLabel('Usuário ou senha incorreta.')
        except Exception:
            self.setStatusLabel('Não foi possível se conectar com o servidor.')
        finally:
            wx.CallAfter(self.disableLoading)

    def _checkExistingSnapshot(self):
        try:
            self._cloudFolder.sync()
            if self._cloudFolder.getTotalFiles() > 0:
                confirm = self._view.showExistingSnapshotDialog()
                if not confirm:
                    self._authService.signout()
                    self._cloudFolder.clear()
                    self.quit()

            self._nextStep()
        except Exception as err:
            print(err)
            self._nextStep()

    def show(self):
        self._view.start()

    def isActive(self):
        return bool(self._view)

    def quit(self):
        self._view.destroy()


class WizardInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.btnSignin.Bind(wx.EVT_BUTTON, self.OnSignin)
        self._view.txtEmail.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter)
        self._view.txtPassword.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter)
        self._view.btnConfirmNfsDir.Bind(wx.EVT_BUTTON, self.OnConfirmNfsDir)
        self._view.nfsDir.Bind(wx.EVT_DIRCTRL_SELECTIONCHANGED, self.OnNfsDirChange)

    def OnSignin(self, evt):
        self._presenter.signin()

    def OnNfsDirChange(self, evt):
        self._presenter.updateModel()

    def OnConfirmNfsDir(self, evt):
        self._presenter.confirmNfsDir()

    def OnPressEnter(self, event):
        self._presenter.signin()
