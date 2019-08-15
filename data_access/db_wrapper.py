""" testing db storage """
import sqlite3
import os.path
from text import token
DEFAULT_DB = "text.db"

class DB_Connection():
    def __init__(self, token_converter, threshold=100, db=DEFAULT_DB):
        self.commands = {
            "add": "INSERT INTO VOCAB (ID, WORD, WORD_COUNT) VALUES (null, ?, ?)",
            "increment": "UPDATE VOCAB SET WORD_COUNT = WORD_COUNT + ? WHERE WORD=?"
        }
        self.queue = {
            "add" : [],
            "increment" : []
        }
        makeDB = not os.path.exists(db)
        self.db_conn = sqlite3.connect(db)
        self._cursor = self.db_conn.cursor()
        if makeDB:
            self._cursor.execute("CREATE TABLE `VOCAB` ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, `WORD` TEXT, `WORD_COUNT` INTEGER )")
        self.threshold = threshold
        self.token_converter = token_converter

    def increment(self, word):
        is_add = not self.is_in(word)
        if (not is_add):
            for key, items in self.queue.items():
                if word in items:
                    pass 
#modify the item so increment is bigger, but should reform command queues first
        #check to see if word is already added, in that case increment it in queue command too
        command = "add" if is_add else "increment"
        inputs = (word, 1) if is_add else (1, word)
        self._queue_command(command, inputs)
    
    def is_in(self, word):
        self._run_command('SELECT * FROM VOCAB WHERE WORD=?', word)
        return bool(self._cursor.fetchone())
    
    def _run_command(self, command, word):
        # convert word to db using token_to_db
        if isinstance(word, token.Token):
            word = word.text
        self._cursor.execute(command, (word,))
        self.db_conn.commit()

    def _run_many_commands(self, command, inputs):
        clean_inputs = []
        for i in inputs:
            to_append = []
            for objs in i:
                to_append.append(objs.text if isinstance(objs, token.Token) else objs)
            clean_inputs.append(tuple(to_append))
        self._cursor.executemany(command, clean_inputs)
        self.db_conn.commit()
        
    def _queue_command(self, command, word):
        self.queue[command].append(word);
        self._check_queue()
    
    def _check_queue(self):
        sum = 0
        for key, item in self.queue.items():
            sum += len(item)
        if sum >= self.threshold:
            self._push_queue()

    def _push_queue(self):
        for command in self.queue.keys():
            self._run_many_commands(self.commands[command], self.queue[command])
        self.db_conn.commit()
        self.queue = {
            "add" : [],
            "increment" : []
        }
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._push_queue()
        self.db_conn.exit()
    

    # on close commit and close
