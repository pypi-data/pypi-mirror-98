import threading


class PrefetchedGenerator(object):
    def __init__(self, generator):
         self._data = generator.next()
         self._generator = generator
         self._ready = True

    def next(self):
        if not self._ready:
            self.prefetch()
        self._ready = False
        return self._data

    def prefetch(self):
        if not self._ready:
            self._data = self._generator.next()
            self._ready = True
            
            
            
class BackgroundGenerator(threading.Thread):
    def __init__(self, generator):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue(1)
        self.generator = generator
        self.daemon = True
        self.start()

    def run(self):
        for item in self.generator:
            self.queue.put(item)
        self.queue.put(None)

    def next(self):
            next_item = self.queue.get()
            if next_item is None:
                 raise StopIteration
            return next_item
            
            

# Alternative 3: Prefetch in c library
