import wx

from ui.assets import icons


def show(parent, blacklistedFolder):
    icon = wx.Icon(str(icons.CLOUD))
    return BlacklistPresenter(BlacklistDialog(parent, 'QuantiSync', icon=icon),
                              BlacklistInteractor(),
                              blacklistedFolder)


class BlacklistDialog(wx.Dialog):

    def __init__(self, parent, title, icon):
        super(BlacklistDialog, self).__init__(parent, title=title, size=(600, 500))
        self.SetIcon(icon)
        self._initLayout()

    def _initLayout(self):
        self.SetBackgroundColour("white")
        self.blacklist = wx.ListCtrl(self, -1,
                                     style=wx.LC_REPORT
                                     # | wx.BORDER_SUNKEN
                                     | wx.BORDER_NONE
                                     | wx.LC_EDIT_LABELS
                                     # | wx.LC_SORT_ASCENDING    # disabling initial auto sort gives a
                                     # | wx.LC_NO_HEADER         # better illustration of col-click sorting
                                     # | wx.LC_VRULES
                                     # | wx.LC_HRULES
                                     # | wx.LC_SINGLE_SEL
                                     )
        self.blacklist.InsertColumn(0, "Arquivo")
        self.blacklist.InsertColumn(1, "Razão")
        self.blacklist.SetColumnWidth(1, 500)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.blacklist, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def insertBlacklistedNf(self, fileName, reason):
        index = self.blacklist.InsertItem(self.blacklist.GetItemCount(), fileName)
        self.blacklist.SetItem(index, 1, reason)

    def quit(self):
        self.Destroy()

    def start(self):
        self.CenterOnScreen()
        self.Raise()
        self.ShowModal()


class BlacklistPresenter:
    def __init__(self, view, interactor, blacklistedFolder):
        self._view = view
        interactor.Install(self, self._view)
        self._blacklistedFolder = blacklistedFolder
        self._populateBlacklist()
        self._view.start()

    def _populateBlacklist(self):
        blacklistedFiles = self._blacklistedFolder.getFiles()

        for fileName in blacklistedFiles:
            reason = self._blacklistedFolder.getReason(fileName)
            self._view.insertBlacklistedNf(fileName, reason)


class BlacklistInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view
