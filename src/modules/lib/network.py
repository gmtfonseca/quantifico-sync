import requests
from ...config.network import HTTP_CONFIG
from queue import Queue


class HttpService:

    def __init__(self, endpoint, url=HTTP_CONFIG['url']):
        self.url = url
        self.endpoint = endpoint
        # TODO - Remover
        self.headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI' +
                        '6IjVkMjIwMmQwOWNhOWJjMjY3MDlmOWUzNiIsIm9yZ2FuaXphY2FvIjoiNWQ' +
                        'xZjk1M2RiNTAzYjczNWQ4YTlmNDE3IiwiaWF0IjoxNTYyNTEwMDQxL' +
                        'CJleHAiOjE1NjI1OTY0NDF9.VdjJiIplWtUfGi-9BJaSHs83VV1Hf-kNLP7eHWFl1vg'}

    def post(self, json):
        response = requests.post(self.url + self.endpoint,
                                 json=json,
                                 headers=self.headers)
        response.raise_for_status()
        return response

    def put(self, json):
        response = requests.put(self.url + self.endpoint,
                                json=json,
                                headers=self.headers)
        response.raise_for_status()
        return response

    def delete(self, json):
        response = requests.delete(self.url + self.endpoint,
                                   json=json,
                                   headers=self.headers)
        response.raise_for_status()
        return response

    def stream(self, data, streamGenerator):
        response = requests.post(self.url + self.endpoint,
                                 data=streamGenerator(data),
                                 headers=self.headers)
        response.raise_for_status()
        return response


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
