import unittest
from quantisync.core.file import Properties


class PropertiesTest(unittest.TestCase):

    def test_inicializacao_por_estado(self):
        """
        Testa se atributos são inicializados corretamente a partir do estado
        """
        fileProperties = Properties.fromState('nf1.XML/1000001.1')
        self.assertEqual(fileProperties.name, 'nf1.XML')
        self.assertEqual(fileProperties.modified, '1000001.1')

    def test_estado(self):
        """
        Testa se estado está sendo capturado corretamente
        """
        properties = Properties('nf1.XML', '1000001.1')
        self.assertEqual(properties.getState(), 'nf1.XML/1000001.1')


if __name__ == '__main__':
    unittest.main()
