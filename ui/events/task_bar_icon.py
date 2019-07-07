import wx

myEVT_UI = wx.NewEventType()
EVT_UI = wx.PyEventBinder(myEVT_UI, 1)


class UIEvent(wx.PyCommandEvent):
    def __init__(self, type, id, value=None):
        wx.PyCommandEvent.__init__(self, type, id)
        self._value = value

    def getValue(self):
        return self._value
