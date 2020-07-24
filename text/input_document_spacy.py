import config
import os
import re
import spacy
from collections import defaultdict
import time

from datetime import datetime
import config
import pymysql

class Word_Pos_Pair():
    def __init__(self, *args):
        if len(args) == 2:
            self.word = args[0]
            self.pos = args[1]
        elif len(args) == 1:
            token = args[0]
            self.word = token.text.lower()
            self.pos = token.pos_
        self.num_pos = config.pos.index(self.pos) + 1
    def __eq__(self, word2):
        return self.word == word2.word and self.pos == word2.pos
    def __hash__(self):
        return hash(repr(self))
    def __repr__(self):
        return str(self)
    def __str__(self):
        return "Word_Pos_Pair('{}','{}')".format(self.word, self.pos)

def reset_db(db):
    """ mainly for testing"""
    cursor = db.cursor()
    cursor.execute("DELETE FROM pos")
    cursor.execute("ALTER TABLE pos AUTO_INCREMENT = 1")
    pos = list(config.pos)
    sql = "INSERT INTO pos (id, pos) VALUES (%s, %s)"
    for p in range(len(pos)):
        cursor.execute(sql, (p+1, pos[p]))
    cursor.execute("DELETE FROM words")
    cursor.execute("ALTER TABLE words AUTO_INCREMENT = 1")
    cursor.execute("DELETE FROM pairings")
    db.commit()


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def update_pairings(word_cache, cursor, pairings): ###
    update = "UPDATE pairings SET freq = freq + %s WHERE word1_id=%s AND word2_id=%s"
    insert = "INSERT INTO pairings (word1_id, word2_id, freq) VALUES (%s, %s, %s)"
    commands = dict()
    commands[update] = []
    commands[insert] = []
    collision_list = []
    for pairing, count in pairings.items():
        ids = (word_cache[pairing[0]], word_cache[pairing[1]])
        is_in = cursor.execute('SELECT * FROM pairings WHERE word1_id=%s AND word2_id=%s', ids)
        if (not bool(is_in)):
            try:
                cursor.execute(insert, (ids[0], ids[1], 0))
            except pymysql.err.IntegrityError as e:
                pass # it's in, just update it
        commands[update].append((count, ids[0], ids[1]))
    cursor.executemany(update, commands[update])
    
def update_db(frequencies, pairings, filename): ###
    """updates the databaase"""
    max_tries = 10
    tries = 0;
    while tries < max_tries:
        try:
            word_cache = dict()
            commands = []
            db = pymysql.connect(host=config.sql_db_host,
                                     user=config.sql_username,
                                     password=config.sql_pw,
                                     db=config.sql_db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            for word in frequencies:
                is_in_db = cursor.execute('SELECT id FROM words WHERE word=%s AND pos=%s', (word.word, word.num_pos))
                if (is_in_db == 0):
                    try:
                        cursor.execute('INSERT INTO words (id, word, pos, freq) VALUES (null, %s, %s, %s)', 
                            (word.word, word.num_pos, frequencies[word]))
                    except pymysql.err.IntegrityError as e:
                        pass #already in but coulnd't find it
                    cursor.execute('SELECT id FROM words WHERE word=%s AND pos=%s', (word.word, word.num_pos))
                    word_id = cursor.fetchone()
                    word_id = word_id["id"]
                else:
                    cursor.execute('SELECT id FROM words WHERE word=%s AND pos=%s', (word.word, word.num_pos))
                    word_id = cursor.fetchone()
                    word_id = word_id["id"]
                word_cache[word] = word_id
            update_pairings(word_cache, db.cursor(), pairings)
            db.commit()
            tries = max_tries
        except pymysql.err.OperationalError as e:
            tries += 1 #deadlock, try again
            if tries == max_tries:
                print("!!! retry {} !!!".format(filename))


def is_english(s):
    """is string english?"""
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    return bool(re.match(r".*[a-zA-Z]", s))

def do_index(token): 
    """Should token be recorded in DB"""
    return (token.pos_ != "PROPN" and (is_english(token.text)))

def extract_data(line): 
    """
    pairings = {(word_pos_pair, word_pos_pair2): count}
    frequencies = {word_pos_pair: count}
    """
    space = spacy.load("en")
    if line == "" or line[0] == "<" or line[0].isnumeric(): return [0,0]
    pairings = defaultdict(int)
    frequencies = defaultdict(int)
    line = space(line)
    for token in line: 
        if do_index(token):
            frequencies[Word_Pos_Pair(token)] += 1
    cap = len(line)
    for ti in range(cap):
        if do_index(line[ti]):
            lower = ti if ti < config.degree_association else config.degree_association
            upper = cap - ti -1 if ti >= cap - config.degree_association -1 else config.degree_association
            # the -1 is because (range(1, 1) won't run once for 1
            for i in range(lower):
                if do_index(line[ti-i-1]):
                    pairings[Word_Pos_Pair(line[ti-i-1]), Word_Pos_Pair(line[ti])] += 1
            for i in range(upper):
                if do_index(line[ti+i+1]):
                    pairings[Word_Pos_Pair(line[ti]), Word_Pos_Pair(line[ti+i+1])] += 1           
    return [pairings, frequencies]


def read_data(file_name): ###
    """ Processes a file """
    try:
        lines = []
        pairings = defaultdict(int)
        frequencies = defaultdict(int)
        with open(file_name) as file:
            lines = file.readlines()
        print("READ      {} {}".format(file_name, now()))
        for line in lines:
            pa, fq = extract_data(line.replace('"', ""))
            if pa != 0: # html line
                for word, count in fq.items():
                    frequencies[word] += count
                for pairing, count in pa.items():
                    pairings[pairing] += count

        print("PROCESSED {} {}".format(file_name, now()))
        update_db(frequencies, pairings, file_name)
        print("UPLOADED  {} {}".format(file_name, now()))
        return True
    except Exception as e:
        return str(e)
