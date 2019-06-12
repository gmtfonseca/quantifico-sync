from queue import Queue


class EstadoQueue:
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.queue = Queue()

    def push(self, estado):
        self.queue.put_nowait(estado)

    def next_batch(self):
        batch = set()
        for i in range(self.batch_size):
            batch.add(self.queue.get())
        return batch

    def size(self):
        return self.queue.qsize()

    def empty(self):
        return self.queue.empty()
