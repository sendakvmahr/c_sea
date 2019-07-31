""" testing db storage """
import sqlite3
DEFAULT_DB = "text.db"
class DB_Connection():
    def __init__(self, threshold=5):
        self.db_cache = set()
        self.db_conn = sqlite3.connect(DEFAULT_DB)
        self._cursor = self.db_conn.cursor()
        self.queue = []
        self.threshold = threshold

    def add(self, word):
        command = "add"
        self._queue_command(command, word)
    
    def set(self, word, value):
        command = "set"
    
    def is_in(self, word):
        print(word)
        if word in (self.db_cache):
            return True;
        self._cursor.execute('SELECT * FROM VOCAB WHERE WORD=?', (word,))
        return self._cursor.fetchone()
        
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
        words = list(w[1].text for w in set(self.queue))
        print(words);
        wordmap = dict()
        commands_insert = []
        commands_update = []
        for word in words:
            wordmap[word] = self.queue.count(word)
            if self.is_in(word):
                commands_insert.append((word, wordmap[word]))
            else:
                commands_update.append((wordmap[word], word))
        self._cursor.executemany("INSERT INTO VOCAB (WORD, WORD_COUNT) VALUES (?, ?)", commands_insert)
        self._cursor.executemany("UPDATE VOCAB SET WORD_COUNT = WORD_COUNT + ? WHERE WORD=?", commands_update)
        self.db_conn.commit()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._push_queue(self)
        self.db_conn.exit()
    

    # on close commit and close
