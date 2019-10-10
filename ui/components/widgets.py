import wx
from ui.assets import colors


class PrimaryButton(wx.Button):
    def __init__(self, parent, label, size=(80, 30)):
        super().__init__(parent, label=label, size=size, style=wx.BORDER_NONE)
        super().SetBackgroundColour(colors.PRIMARY)
        super().SetForegroundColour('white')
