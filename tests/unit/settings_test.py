import unittest
from unittest.mock import Mock

from tests.config import FIXTURE_PATH
from quantisync.core.settings import Settings, SettingsSerializer


class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.settingsPath = FIXTURE_PATH / 'settings.json'
        self.settingsSerializer = SettingsSerializer(self.settingsPath)

    def tearDown(self):
        self.settingsPath.unlink()

    def test_save_json(self):
        """
        Testa se json é criado corretamente
        """
        settings = Settings(nfsDir='path/to/file')
        self.settingsSerializer.save(settings)
        self.assertTrue(self.settingsPath.exists())

    def test_load_json(self):
        """
        Testa se objeto Settings é carregado corretamente
        """
        savedSettings = Settings(nfsDir='path/to/file')
        self.settingsSerializer.save(savedSettings)

        loadedSettings = self.settingsSerializer.load()
        self.assertEqual(savedSettings.nfsDir, loadedSettings.nfsDir)


if __name__ == '__main__':
    unittest.main()
