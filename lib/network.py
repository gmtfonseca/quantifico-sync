import requests
from config.network import HTTP_CONFIG
from queue import Queue


class HttpService:

    def __init__(self, endpoint, url=HTTP_CONFIG['url']):
        self.url = url
        self.endpoint = endpoint

    def post(self, json):
        response = requests.post(self.url + self.endpoint, json=json).json()
        return response

    def put(self, json):
        response = requests.put(self.url + self.endpoint, json=json).json()
        return response

    def delete(self, json):
        response = requests.delete(self.url + self.endpoint, json=json).json()
        return response

    def stream(self, data, streamGenerator):
        response = requests.post(
            self.url + self.endpoint, data=streamGenerator(data)).json()
        return response


class HttpRequestQueue:
    def __init__(self, httpService, batch_size):
        self._httpService = httpService
        self._batch_size = batch_size
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
            self.postBatchHandler(response)

    def _handleHttpRequest(self):
        pass

    def _nextBatch(self):
        batch = []
        i = 0
        while i < self.batch_size and not self.empty():
            batch.append(self._queue.get())
            i += 1
        return batch

    def pending(self):
        return self._queue.qsize()


class HttpStreamQueue(HttpRequestQueue):
    def __init__(self, httpService, batch_size, streamGenerator):
        super().__init__(httpService, batch_size)
        self.streamGenerator = streamGenerator

    def _handleHttpRequest(self, batch):
        return self._httpService.stream(batch, self.streamGenerator)


class HttpDeleteQueue(HttpRequestQueue):
    def __init__(self, httpService, batch_size):
        super().__init__(httpService, batch_size)

    def _handleHttpRequest(self, batch):
        return self._httpService.delete(batch)
