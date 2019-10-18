import wx

myEVT_SYNC = wx.NewEventType()
EVT_SYNC = wx.PyEventBinder(myEVT_SYNC, 2)


class SyncEvent(wx.PyCommandEvent):
    def __init__(self, type, id, state):
        wx.PyCommandEvent.__init__(self, type, id)
        self._state = state

    @property
    def state(self):
        return self._state
