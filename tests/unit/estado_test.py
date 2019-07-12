import unittest
from unittest.mock import Mock

from quantisync.core.estado import Cliente, Servidor, Observador
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


class ObservadorTest(unittest.TestCase):

    def test_deteccao_insercoes(self):
        """
        Testa se inserções são detectadas corretamente
        """
        servidorMock = Mock()
        servidorMock.getEstado.return_value = {'2859/1551545907.0'}
        clienteMock = Mock()
        clienteMock.getEstado.return_value = {
            '2859/1551545907.0',
            '2865/1551545907.0',
        }
        observador = Observador(clienteMock, servidorMock)
        observador.observar()
        self.assertTrue(observador.possuiInsercoes())
        self.assertEqual(observador.getInsercoes(), {'2865/1551545907.0'})

    def test_deteccao_remocoes(self):
        """
        Testa se inserções são detectadas corretamente
        """
        servidorMock = Mock()
        servidorMock.getEstado.return_value = {
            '2859/1551545907.0',
            '2865/1551545907.0'
        }
        clienteMock = Mock()
        clienteMock.getEstado.return_value = {'2859/1551545907.0'}
        observador = Observador(clienteMock, servidorMock)
        observador.observar()
        self.assertTrue(observador.possuiRemocoes())
        self.assertEqual(observador.getRemocoes(), {'2865/1551545907.0'})


if __name__ == '__main__':
    unittest.main()
