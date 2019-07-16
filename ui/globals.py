from quantisync.core.sync import SyncManager
from quantisync.lib.factory import SyncFactory

syncManager = {}


def createSyncManager(view):
    global syncManager
    syncManager = SyncManager(SyncFactory(view))
    syncManager.createSync()
