import wx

myEVT_UI = wx.NewEventType()
EVT_UI = wx.PyEventBinder(myEVT_UI, 1)


class UIEvent(wx.PyCommandEvent):
    def __init__(self, type, id, estado, isFatal):
        wx.PyCommandEvent.__init__(self, type, id)
        self._estado = estado
        self._isFatal = isFatal

    def getEstado(self):
        return self._estado

    def isFatal(self):
        return self._isFatal
