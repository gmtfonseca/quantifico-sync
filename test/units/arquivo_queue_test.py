import unittest
from modules.arquivo_queue import ArquivoQueue
from unittest.mock import Mock

BATCH_SIZE = 2


class ArquivoQueueTest(unittest.TestCase):

    def testa_enqueue(self):
        """
        Testa enqueue
        """
        arquivo = Mock()
        arquivoQueue = ArquivoQueue(BATCH_SIZE)
        arquivoQueue.enqueue(arquivo)
        self.assertTrue(arquivoQueue.size() > 0)

    def testa_in_next_batch(self):
        """
        Testa se arquivo está na próxima batch
        """
        arquivo1 = Mock()
        arquivo2 = Mock()
        arquivoQueue = ArquivoQueue(BATCH_SIZE)
        arquivoQueue.enqueue(arquivo1)
        arquivoQueue.enqueue(arquivo2)
        self.assertIn(arquivo2, arquivoQueue.nextBatch())

    def testa_not_in_next_batch(self):
        """
        Testa se arquivo não está na próxima batch
        """
        arquivo1 = Mock()
        arquivo2 = Mock()
        arquivo3 = Mock()
        arquivoQueue = ArquivoQueue(BATCH_SIZE)
        arquivoQueue.enqueue(arquivo1).enqueue(arquivo2).enqueue(arquivo3)
        self.assertNotIn(arquivo3, arquivoQueue.nextBatch())

    def testa_empty(self):
        """
        Testa empty
        """
        arquivo1 = Mock()
        arquivo2 = Mock()
        arquivoQueue = ArquivoQueue(BATCH_SIZE)
        arquivoQueue.enqueue(arquivo1).enqueue(arquivo2)
        arquivoQueue.nextBatch()
        self.assertTrue(arquivoQueue.empty())


if __name__ == '__main__':
    unittest.main()
