import unittest
from unittest import mock
from datetime import datetime
# from unittest.mock import Mock

from quantisync.lib.util import File
from quantisync.core.model import SyncDataModel, UnableToSaveError
from tests.config import FIXTURE_PATH


SYNC_DATA_PATH = FIXTURE_PATH / 'sync_data.json'


class SyncDataModelTest(unittest.TestCase):
    def setUp(self):
        File(SYNC_DATA_PATH).unlink()

    def test_set_last_sync(self):
        syncDataModel = SyncDataModel(SYNC_DATA_PATH)
        lastSync = datetime.now()
        syncDataModel.setLastSync(lastSync)
        syncData = syncDataModel.getSyncData()
        self.assertEquals(syncData.lastSync, lastSync)

    def test_set_nf_dir(self):
        nfsDir = 'C:/'
        syncDataModel = SyncDataModel(SYNC_DATA_PATH)
        syncDataModel.setNfsDir(nfsDir)
        syncData = syncDataModel.getSyncData()
        self.assertEquals(syncData.nfsDir, nfsDir)

    def test_set_user(self):
        userEmail = 'x@gmail.com'
        userOrg = 'Company'
        syncDataModel = SyncDataModel(SYNC_DATA_PATH)
        syncDataModel.setUser(userEmail, userOrg)
        syncData = syncDataModel.getSyncData()
        self.assertEquals(syncData.userEmail, userEmail)
        self.assertEquals(syncData.userOrg, userOrg)

    def test_multiple_set(self):
        nfsDir = 'C:/'
        userEmail = 'x@gmail.com'
        userOrg = 'Company'
        lastSync = datetime.now()
        syncDataModel = SyncDataModel(SYNC_DATA_PATH)
        syncDataModel.setNfsDir('C:/')
        syncDataModel.setUser('x@gmail.com', 'Company')
        syncDataModel.setLastSync(lastSync)
        syncData = syncDataModel.getSyncData()
        self.assertEquals(syncData.nfsDir, nfsDir)
        self.assertEquals(syncData.userEmail, userEmail)
        self.assertEquals(syncData.userOrg, userOrg)
        self.assertEquals(syncData.lastSync, lastSync)

    def test_date_deserialization(self):
        lastSync = datetime.now()
        syncDataModel = SyncDataModel(SYNC_DATA_PATH)
        syncDataModel.setLastSync(lastSync)
        syncDataModelCopy = SyncDataModel(SYNC_DATA_PATH)
        syncData = syncDataModelCopy.getSyncData()
        self.assertEquals(syncData.lastSync, lastSync)

    def test_remove(self):
        lastSync = datetime.now()
        syncDataModel = SyncDataModel(SYNC_DATA_PATH)
        syncDataModel.setLastSync(lastSync)
        syncDataModel.remove()
        self.assertFalse(File(syncDataModel.jsonPath).exists())

    @mock.patch('quantisync.core.model.json.dump')
    def test_save_throws_exception(self, jsonDump):
        jsonDump.side_effect = Exception()
        nfsDir = 'C:/'
        with self.assertRaises(UnableToSaveError):
            syncDataModel = SyncDataModel(SYNC_DATA_PATH)
            syncDataModel.setNfsDir(nfsDir)


if __name__ == '__main__':
    unittest.main()
