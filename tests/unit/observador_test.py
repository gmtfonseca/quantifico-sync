import unittest
from unittest.mock import Mock

from quantisync.core.estado import Observador


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
