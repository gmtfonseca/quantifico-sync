import wx

myEVT_SYNC = wx.NewEventType()
EVT_SYNC = wx.PyEventBinder(myEVT_SYNC, 2)


class SyncEvent(wx.PyCommandEvent):
    def __init__(self, type, id, state, isFatal):
        wx.PyCommandEvent.__init__(self, type, id)
        self._state = state
        self._isFatal = isFatal

    def getState(self):
        return self._state

    def isFatal(self):
        return self._isFatal
