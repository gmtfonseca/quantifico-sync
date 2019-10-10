import wx
from ui.assets import colors


class PrimaryButton(wx.Button):
    def __init__(self, parent, label, size=(80, 30), id=wx.ID_ANY):
        super().__init__(parent, label=label, size=size, style=wx.BORDER_NONE, id=id)
        super().SetBackgroundColour(colors.PRIMARY)
        super().SetForegroundColour('white')
