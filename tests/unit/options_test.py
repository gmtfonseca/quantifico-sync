import unittest
from unittest.mock import Mock

from tests.config import FIXTURE_PATH
from quantisync.core.options import Options, OptionsSerializer


class OptionsTest(unittest.TestCase):

    def setUp(self):
        self.optionsPath = FIXTURE_PATH / 'options.json'
        self.optionsSerializer = OptionsSerializer(Mock(), self.optionsPath)

    def tearDown(self):
        self.optionsPath.unlink()

    def test_save_json(self):
        """
        Testa se json é criado corretamente
        """
        options = Options(nfsPath='path/to/file')
        self.optionsSerializer.save(options)
        self.assertTrue(self.optionsPath.exists())

    def test_load_json(self):
        """
        Testa se objeto Options é carregado corretamente
        """
        optionsSaved = Options(nfsPath='path/to/file')
        self.optionsSerializer.save(optionsSaved)

        optionsLoaded = self.optionsSerializer.load()
        self.assertEqual(optionsSaved.nfsPath, optionsLoaded.nfsPath)


if __name__ == '__main__':
    unittest.main()
