import unittest

from quantisync.core.estado import Cliente, Servidor
from tests.config import FIXTURE_PATH


class ClienteTest(unittest.TestCase):

    def test_inicializacao_estado(self):
        """
        Testa se estado é iniciado corretamente
        """
        estadoCorreto = {
            'valid1/1562953320.685',
            'valid2/1562953323.189'
        }
        cliente = Cliente(FIXTURE_PATH / 'cliente', 'XML')
        self.assertEqual(cliente.getEstado(), estadoCorreto)


class ServidorTest(unittest.TestCase):

    def test_inicializacao_estado(self):
        """
        Testa se estado é iniciado corretamente
        """
        estadoCorreto = {
            '2859/1551545907.0',
            '2865/1551545907.0',
        }
        servidor = Servidor(FIXTURE_PATH / 'quantisync.dat')
        self.assertEqual(servidor.getEstado(), estadoCorreto)


if __name__ == '__main__':
    unittest.main()
