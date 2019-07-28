""" testing db storage """

class DB_Connection():
    def __init__(self, threshold=100):
        self.db = set()
        self.queue = []
        self.threshold = threshold

    def add(self, word):
        command = "add"
        self._queue_command("add", word)
    
    def set(self, word, value):
        command = "set"
    
    def is_in(self, word):
        self.conn

    def _queue_command(self, command, word):
        self.queue.append((command, word))
        self._check_queue()
    
    def count(self):
        return len(self.db)

    def _check_queue(self):
        if len(self.queue) == self.threshold:
            self._push_queue()

    def _push_queue(self):
        # if there's multiple adds of a word, unify them into set word = # of instances
        # then, for each word, check if it's in teh database (cache later). if it's in, set it to increment instead of addword 
        # push all teh queues through in a massive queue list
        pass
