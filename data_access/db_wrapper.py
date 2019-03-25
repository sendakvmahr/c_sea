""" testing db storage """

class DB_Connection():
    def __init__(self, threshold=100):
        self.db = set()
        self.queue = []
        self.threshold = threshold

    def add(self, word):
        command = "if word is there then increment else initialize with 1?"
        self._queue_command()
    
    def set(self, word, value):
        command = ""

    def _queue_command(self, item, count):
        self.queue.append(command)
        self._check_queue()
    
    def count(self):
        return len(self.db)

    def _check_queue(self):
        if len(self.queue == threshold):
            self._push_queue()

    def _push_queue(self):
        # make a query based on self.queue
        # push it through 
        pass
