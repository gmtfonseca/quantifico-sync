import unittest
import os
from core.estado import Cliente, Servidor


class ClienteTest(unittest.TestCase):

    def test_inicializacao_estado(self):
        """
        Testa se estado é iniciado corretamente
        """
        estadoCorreto = {
            '2859/1561936295.8213189',
            '2865/1561936295.8394666'
        }
        PATH = os.path.abspath('tests/fixture/xml')
        EXTENSAO = 'XML'
        cliente = Cliente(PATH, EXTENSAO)
        cliente.carregaEstado()

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
        path = os.path.abspath('tests/fixture/pickle/quantisync.dat')
        servidor = Servidor(path)
        self.assertEqual(servidor.getEstado(), estadoCorreto)


if __name__ == '__main__':
    unittest.main()
