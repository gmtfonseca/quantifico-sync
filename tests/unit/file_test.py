import unittest
from quantisync.core.file import Properties


class PropertiesTest(unittest.TestCase):

    def test_inicializacao_por_estado(self):
        """
        Testa se atributos são inicializados corretamente a partir do estado
        """
        properties = Properties.fromState('2030/1000001.1')
        self.assertEqual(properties.name(), '2030')
        self.assertEqual(properties.modified(), '1000001.1')

    def test_estado(self):
        """
        Testa se estado está sendo capturado corretamente
        """
        properties = Properties('2030', '1000001.1')
        self.assertEqual(properties.getState(), '2030/1000001.1')


if __name__ == '__main__':
    unittest.main()
