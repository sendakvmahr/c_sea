""" testing db storage """
import sqlite3
DEFAULT_DB = "text.db"
class DB_Connection():
    def __init__(self, threshold=5, db=DEFAULT_DB):
        self.commands = {
            "add": "INSERT INTO VOCAB (WORD, WORD_COUNT) VALUES (?, ?)",
            "increment": "INSERT INTO VOCAB (WORD, WORD_COUNT) VALUES (?, ?)"
        }
        self.queue = {}
        # check if db exists, if not, initialize schema
        self.db_conn = sqlite3.connect(db)
        self._cursor = self.db_conn.cursor()
        self.threshold = threshold

    def increment(self, word):
        command = self.is_in(word) ? "increment" : "add"
        self._queue_command(command, word)
    
    def is_in(self, word):
        self._run_command('SELECT * FROM VOCAB WHERE WORD=?', word)
        return self._cursor.fetchone()
    
    def _run_command(self, command, word):
        # convert word to db using token_to_db
        return self._cursor.execute(command, (word,))
        
    def _queue_command(self, command, word):
        self.queue[command].append(word);
        self._check_queue()
    
    def _check_queue(self):
        sum = 0
        for key, item in self.queue.items();
            sum += len(item)
        if sum >= self.threshold:
            self._push_queue()

    def _push_queue(self):
        for command, keys in self.queue:
            self._cursor.executemany(command, keys)
        self.db_conn.commit()
        self.queue = {}
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._push_queue()
        self.db_conn.exit()
    

    # on close commit and close
