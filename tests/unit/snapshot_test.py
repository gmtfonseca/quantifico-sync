import unittest
from unittest.mock import Mock

from quantisync.core.snapshot import LocalFolder, CloudFolder, BlacklistedFolder
from quantisync.core.file import Properties
from quantisync.lib.util import File


from tests.config import FIXTURE_PATH

nfs1 = {'name': 'nfs1.XML',
        'state': '{}/{}'.format('nfs1.XML', File(FIXTURE_PATH / 'local/nfs1.XML').modified()),
        'path': FIXTURE_PATH / 'local/nfs1.XML'}


nfs2 = {'name': 'nfs2.XML',
        'state': '{}/{}'.format('nfs2.XML', File(FIXTURE_PATH / 'local/nfs2.XML').modified()),
        'path': FIXTURE_PATH / 'local/nfs2.XML'}


class LocalFolderTest(unittest.TestCase):

    def test_init(self):
        blacklistedFolder = Mock()
        blacklistedFolder.getSnapshot.return_value = set()
        localFolder = LocalFolder('path', 'extension', blacklistedFolder)
        self.assertEqual(localFolder.getPath(), 'path')
        self.assertEqual(localFolder.getExtension(), 'extension')
        self.assertEqual(localFolder.getSnapshot(), set())

    def test_refresh(self):
        blacklistedFolder = Mock()
        blacklistedFolder.getSnapshot.return_value = set()
        localFolder = LocalFolder(FIXTURE_PATH / 'local', 'XML', blacklistedFolder)
        localFolder.refresh()
        self.assertEqual(localFolder.getSnapshot(), {nfs1['state'], nfs2['state']})

    def test_refresh_with_invalid_file(self):
        blacklistedFolder = Mock()
        blacklistedFolder.getSnapshot.return_value = {nfs1['state']}
        localFolder = LocalFolder(FIXTURE_PATH / 'local', 'XML', blacklistedFolder)
        localFolder.refresh()
        self.assertEqual(localFolder.getSnapshot(), {nfs2['state']})
        self.assertEqual(localFolder.getInvalidSnapshot(), {nfs1['state']})


class CloudFolderTest(unittest.TestCase):

    def setUp(self):
        self.path = FIXTURE_PATH / 'cloud.dat'

    def tearDown(self):
        File(self.path).unlink()

    def test_init(self):
        cloudFolder = CloudFolder(self.path)
        self.assertEqual(cloudFolder.getPath(), self.path)
        self.assertEqual(cloudFolder.getSnapshot(), set())
        self.assertTrue(File(cloudFolder.getPath()).exists())

    def test_set_snapshot(self):
        cloudFolder = CloudFolder(self.path)
        snapshot = {nfs1['state']}
        cloudFolder.setSnapshot(snapshot)
        self.assertEqual(cloudFolder.getSnapshot(), snapshot)


class BlacklistedFolderTest(unittest.TestCase):

    def setUp(self):
        self.path = FIXTURE_PATH / 'blacklisted.dat'

    def tearDown(self):
        File(self.path).unlink()

    def test_add(self):
        blacklistedFolder = BlacklistedFolder(self.path)
        fileName = '1.XML'
        fileProperties = Properties(fileName, 1)
        blacklistedFolder.addFile(fileProperties, 'Invalid')
        self.assertTrue(blacklistedFolder.hasFile(fileName))

    def test_remove(self):
        blacklistedFolder = BlacklistedFolder(self.path)
        fileName = '1.XML'
        fileProperties = Properties(fileName, 1)
        blacklistedFolder.addFile(fileProperties, 'Invalid')
        blacklistedFolder.removeFile(fileName)
        self.assertFalse(blacklistedFolder.hasFile(fileName))

    def test_get_snapshot(self):
        snapshot = {'1.XML/1', '2.XML/1', '3.XML/1'}
        blacklistedFolder = BlacklistedFolder(self.path)
        blacklistedFolder.addFile(Properties('1.XML', 1), 'Invalid')
        blacklistedFolder.addFile(Properties('2.XML', 1), 'Invalid')
        blacklistedFolder.addFile(Properties('3.XML', 1), 'Invalid')
        self.assertEquals(blacklistedFolder.getSnapshot(), snapshot)


class ObserverTest(unittest.TestCase):

    def test_has_changed(self):
        pass

    def test_has_insertions(self):
        pass

    def test_has_deletions(self):
        pass


if __name__ == '__main__':
    unittest.main()
