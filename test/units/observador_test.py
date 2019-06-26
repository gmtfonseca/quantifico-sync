import unittest
from classes.observador import Observador
from unittest.mock import Mock


class ObservadorTest(unittest.TestCase):

    def testa_deteccao_insercoes(self):
        """
        Testa se inserções são detectadas corretamente
        """
        servidorMock = Mock()
        servidorMock.getEstado.return_value = {
            '2859/1551545907.0',
        }
        clienteMock = Mock()
        clienteMock.getEstado.return_value = {
            '2859/1551545907.0',
            '2865/1551545907.0',
        }
        mockHandler = Mock()
        observador = Observador(mockHandler, clienteMock, servidorMock)
        observador.detectaMudancas()
        mockHandler.onInsercao.assert_called_with(
            clienteMock, servidorMock, {'2865/1551545907.0'})

    def testa_deteccao_remocoes(self):
        """
        Testa se inserções são detectadas corretamente
        """
        servidorMock = Mock()
        servidorMock.getEstado.return_value = {
            '2859/1551545907.0',
            '2865/1551545907.0',
        }
        clienteMock = Mock()
        clienteMock.getEstado.return_value = {
            '2859/1551545907.0'
        }
        mockHandler = Mock()
        observador = Observador(mockHandler, clienteMock, servidorMock)
        observador.detectaMudancas()
        mockHandler.onRemocao.assert_called_with(
            servidorMock, {'2865/1551545907.0'})


if __name__ == '__main__':
    unittest.main()
