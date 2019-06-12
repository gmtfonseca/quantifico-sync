from queue import Queue


class ArquivoQueue:
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.queue = Queue()

    def enqueue(self, arquivo):
        self.queue.put_nowait(arquivo)

    def nextBatch(self):
        batch = []
        i = 0
        while i < self.batch_size and not self.empty():
            batch.append(self.queue.get())
            i += 1
        return batch

    def size(self):
        return self.queue.qsize()

    def empty(self):
        return self.queue.empty()
