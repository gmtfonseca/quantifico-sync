from quantisync.core.sync import SyncManager
from quantisync.lib.factory import SyncFactory

syncManager = None


def createSyncManager(view):
    global syncManager
    syncManager = SyncManager(SyncFactory(view))
