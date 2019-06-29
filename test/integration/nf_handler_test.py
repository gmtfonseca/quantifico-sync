import unittest
import os
from classes.nf_handler import NfHandler
from classes.estado import Cliente, Servidor
from unittest.mock import Mock

NF_PATH = os.path.abspath('test/fixture/xml')
PICKLE_PATH = os.path.abspath(
    'test/fixture/pickle/temp.dat')


class NfHandlerTest(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(NF_PATH)
        self.servidor = Servidor(PICKLE_PATH)

    def tearDown(self):
        os.remove(self.servidor.getPath())

    def testa_mudanca_estado_servidor_insercao(self):
        """
        Testa se estado servidor é atualizado corretamente após inserção
        """
        insercoes = {
            '2859/1551545907.0',
            '2865/1551541907.0'
        }
        httpService = Mock()
        httpService.stream.return_value = insercoes
        nfHandler = NfHandler(httpService)
        nfHandler.onInsercao(self.cliente, self.servidor, insercoes)
        self.assertEqual(self.servidor.getEstado(), insercoes)

    def testa_mudanca_estado_servidor_remocao(self):
        """
        Testa se estado servidor é atualizado corretamente após remoçao
        """
        remocoes = {'2859/1551545907.0'}
        estadoServidor = {'2865/1551541907.0'}
        httpService = Mock()
        httpService.delete.return_value = estadoServidor
        nfHandler = NfHandler(httpService)
        nfHandler.onRemocao(self.servidor, remocoes)
        self.assertEqual(self.servidor.getEstado(), estadoServidor)


if __name__ == '__main__':
    unittest.main()
