import unittest
from modules.arquivo import PropriedadesArquivo


class PropriedadesArquivoTest(unittest.TestCase):

    def testa_inicializacao_por_estado(self):
        """
        Testa se atributos são inicializados corretamente a partir do estado
        """
        arquivo = PropriedadesArquivo.fromEstado('2030/1000001.1')
        self.assertEqual(arquivo.nome, '2030')
        self.assertEqual(arquivo.dataModificacaoSegundos, 1000001.1)

    def testa_estado(self):
        """
        Testa se estado está sendo capturado corretamente
        """
        arquivo = PropriedadesArquivo('2030', 1000001.1)
        self.assertEqual(arquivo.getEstado(), '2030/1000001.1')


if __name__ == '__main__':
    unittest.main()
