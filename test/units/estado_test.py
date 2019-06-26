import unittest
import os
from classes.estado import Cliente, Servidor


class ClienteTest(unittest.TestCase):

    def testa_inicializacao_estado(self):
        """
        Testa se estado é iniciado corretamente
        """
        estadoCorreto = {
            '2859/1551545907.0',
            '2865/1551545907.0'
        }
        path = os.path.abspath('test/fixture/xml')
        cliente = Cliente(path)
        cliente.atualizar()

        self.assertEqual(cliente.getEstado(), estadoCorreto)


class ServidorTest(unittest.TestCase):

    def testa_inicializacao_estado(self):
        """
        Testa se estado é iniciado corretamente
        """
        estadoCorreto = {
            '2859/1551545907.0',
            '2865/1551545907.0',
        }
        path = os.path.abspath('test/fixture/pickle/quantisync.dat')
        servidor = Servidor(path)
        self.assertEqual(servidor.getEstado(), estadoCorreto)


if __name__ == '__main__':
    unittest.main()
