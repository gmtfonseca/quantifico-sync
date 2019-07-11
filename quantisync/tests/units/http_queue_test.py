import unittest
from lib.network import HttpRequestQueue, HttpDeleteQueue, HttpStreamQueue
from unittest.mock import Mock

BATCH_SIZE = 2


class HttpRequestQueueTest(unittest.TestCase):

    def test_enqueue(self):
        """
        Testa enqueue
        """
        arquivo = Mock()
        httpService = Mock()
        httpRequestQueue = HttpRequestQueue(httpService, BATCH_SIZE)
        httpRequestQueue.enqueue(arquivo)
        self.assertTrue(httpRequestQueue.pending() == 1)

    def test_dequeue_pending(self):
        """
        Testa remoção de elemeto ao realizar dequeue
        """
        httpService = Mock()
        nf = Mock()
        httpRequestQueue = HttpRequestQueue(httpService, BATCH_SIZE)
        httpRequestQueue.enqueue(nf)

        def postBatchHandler(response):
            pass

        httpRequestQueue.dequeue(postBatchHandler)
        self.assertEqual(httpRequestQueue.pending(), 0)


class HttpDeleteQueueTest(unittest.TestCase):

    def test_post_batch_handler(self):
        """
        Testa chamada de handler após envio de batch
        """
        httpResponseMock = {'mock/1111'}
        httpService = Mock()
        httpService.delete.return_value = httpResponseMock
        httpDeleteQueue = HttpDeleteQueue(httpService)
        nf = Mock()
        httpDeleteQueue.enqueue(nf)

        def postBatchHandler(response):
            self.assertEqual(httpResponseMock, response)

        httpDeleteQueue.dequeue(postBatchHandler)


class HttpStreamQueueTest(unittest.TestCase):

    def test_post_batch_handler(self):
        """
        Testa chamada de handler após envio de batch
        """
        httpResponseMock = {'mock/1111'}
        httpService = Mock()
        httpService.stream.return_value = httpResponseMock
        streamGenerator = Mock()
        httpStreamQueue = HttpStreamQueue(httpService, streamGenerator)
        nf = Mock()
        httpStreamQueue.enqueue(nf)

        def postBatchHandler(response):
            self.assertEqual(httpResponseMock, response)

        httpStreamQueue.dequeue(postBatchHandler)


if __name__ == '__main__':
    unittest.main()
