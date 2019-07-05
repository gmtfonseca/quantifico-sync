import logging
import requests
from config.network import HTTP_CONFIG
from queue import Queue


class HttpService:

    def __init__(self, endpoint, url=HTTP_CONFIG['url']):
        self.url = url
        self.endpoint = endpoint
        # TODO - Remover
        self.headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.' +
                        'eyJpZCI6IjVkMWY5NWFiYjUwM2I3MzVkOGE5ZjQxOCIsIm9yZ2FuaXphY2F' +
                        'vIjoiNWQxZjk1M2RiNTAzYjczNWQ4YTlmNDE3IiwiaWF0IjoxNTYyMzYzODY' +
                        '4LCJleHAiOjE1NjI0NTAyNjh9.eCWopiB6ACL6kyoAcbDbOW9-mOpMGIjBW5HLMsdzjCs'}

    def post(self, json):
        try:
            response = requests.post(self.url + self.endpoint,
                                     json=json,
                                     headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as error:
            logging.debug(error)

    def put(self, json):
        try:
            response = requests.put(self.url + self.endpoint,
                                    json=json,
                                    headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as error:
            logging.debug(error)

    def delete(self, json):
        try:
            response = requests.delete(self.url + self.endpoint,
                                       json=json,
                                       headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as error:
            logging.debug(error)

    def stream(self, data, streamGenerator):
        try:
            response = requests.post(self.url + self.endpoint,
                                     data=streamGenerator(data),
                                     headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as error:
            logging.debug(error)


class HttpRequestQueue:
    """
    Estrutura de dados responável em realizar requisições HTTP em batches
    """

    def __init__(self, httpService, batchSize):
        self._httpService = httpService
        self._batchSize = batchSize
        self._queue = Queue()

    def enqueue(self, arquivo):
        self._queue.put_nowait(arquivo)
        return self

    def dequeue(self, postBatchHandler):
        """
        Realiza chamadas HTTP dos elementos da fila em batches
        """
        while not self._queue.empty():
            nextBatch = self._nextBatch()
            response = self._handleHttpRequest(nextBatch)
            postBatchHandler(response)

    def _handleHttpRequest(self, batch):
        pass

    def _nextBatch(self):
        batch = []
        i = 0
        while i < self._batchSize and not self._queue.empty():
            batch.append(self._queue.get())
            i += 1
        return batch

    def pending(self):
        return self._queue.qsize()


class HttpStreamQueue(HttpRequestQueue):
    def __init__(self, httpService, streamGenerator, batchSize=HTTP_CONFIG['MAX_BATCH_SIZE']['STREAM']):
        super().__init__(httpService, batchSize)
        self.streamGenerator = streamGenerator

    def _handleHttpRequest(self, batch):
        return self._httpService.stream(batch, self.streamGenerator)


class HttpDeleteQueue(HttpRequestQueue):
    def __init__(self, httpService, batchSize=HTTP_CONFIG['MAX_BATCH_SIZE']['DELETE']):
        super().__init__(httpService, batchSize)

    def _handleHttpRequest(self, batch):
        return self._httpService.delete(batch)
