import unittest
from datetime import datetime
# from unittest.mock import Mock

from quantisync.core.model import SettingsModel


class SettingsTest(unittest.TestCase):
    def setUp(self):
        if SettingsModel.table_exists():
            SettingsModel.delete()

    def test_set_last_sync(self):
        lastSync = datetime.now()
        SettingsModel.setLastSync(lastSync)
        settings = SettingsModel.select().execute()
        self.assertTrue(settings[0].last_sync == lastSync)

    def test_set_nf_dir(self):
        nfsDir = 'C:/'
        SettingsModel.setNfsDir(nfsDir)
        settings = SettingsModel.select().execute()
        self.assertTrue(settings[0].nfs_dir == nfsDir)

    def test_set_user(self):
        userEmail = 'x@gmail.com'
        userOrg = 'Company'
        SettingsModel.setUser(userEmail, userOrg)
        settings = SettingsModel.select().execute()
        self.assertTrue(settings[0].user_email == userEmail)
        self.assertTrue(settings[0].user_org == userOrg)

    def test_get(self):
        nfsDir = 'C:/'
        userEmail = 'x@gmail.com'
        userOrg = 'Company'
        lastSync = datetime.now()
        SettingsModel.setNfsDir('C:/')
        SettingsModel.setUser('x@gmail.com', 'Company')
        SettingsModel.setLastSync(lastSync)
        settings = SettingsModel.get()
        self.assertEquals(settings.nfsDir, nfsDir)
        self.assertEquals(settings.userEmail, userEmail)
        self.assertEquals(settings.userOrg, userOrg)
        self.assertEquals(settings.lastSync, lastSync)

    def test_table_creation(self):
        SettingsModel.drop_table()
        SettingsModel.setLastSync(datetime.now())
        self.assertTrue(SettingsModel.table_exists())
        SettingsModel.drop_table()
        SettingsModel.setNfsDir('C:/')
        self.assertTrue(SettingsModel.table_exists())
        SettingsModel.drop_table()
        SettingsModel.setUser('x@gmail.com', 'Company')
        self.assertTrue(SettingsModel.table_exists())

    def test_single_record(self):
        SettingsModel.setLastSync(datetime.now())
        SettingsModel.setNfsDir('C:/')
        SettingsModel.setUser('x@gmail.com', 'Company')
        settings = SettingsModel.select().execute()
        self.assertTrue(len(settings) == 1)


if __name__ == '__main__':
    unittest.main()
