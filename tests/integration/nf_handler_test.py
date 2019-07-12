import unittest
import os
from unittest.mock import Mock

from quantisync.core.nf.nf_handler import NfHandler
from quantisync.core.estado import Cliente, Servidor
from tests.shared.mock import MockResponse
from tests.config import FIXTURE_PATH


class NfHandlerTest(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(FIXTURE_PATH / 'cliente', 'XML')
        self.servidor = Servidor(FIXTURE_PATH / 'temp.dat')

    def tearDown(self):
        os.remove(self.servidor.getPath())

    def test_mudanca_estado_servidor_insercao(self):
        """
        Testa se estado servidor é atualizado corretamente após inserção
        """
        insercoes = {
            'valid1/1551545907.0',
            'valid2/1551541907.0'
        }
        response = MockResponse(insercoes, 200)
        httpService = Mock()
        httpService.stream.return_value = response
        nfHandler = NfHandler(httpService)
        nfHandler.onInsercao(self.cliente, self.servidor, insercoes)
        self.assertEqual(self.servidor.getEstado(), insercoes)

    def test_mudanca_estado_servidor_remocao(self):
        """
        Testa se estado servidor é atualizado corretamente após remoçao
        """
        remocoes = {'valid1/1551545907.0'}
        estadoServidor = {'valid2/1551541907.0'}
        response = MockResponse(estadoServidor, 200)
        httpService = Mock()
        httpService.delete.return_value = response
        nfHandler = NfHandler(httpService)
        nfHandler.onRemocao(self.servidor, remocoes)
        self.assertEqual(self.servidor.getEstado(), estadoServidor)


if __name__ == '__main__':
    unittest.main()
