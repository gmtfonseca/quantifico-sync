from quantisync.core.sync import SyncManager

syncManager = None


def createSyncManager(syncFactory):
    global syncManager
    syncManager = SyncManager(syncFactory)
