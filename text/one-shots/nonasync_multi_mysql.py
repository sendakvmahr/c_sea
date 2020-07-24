import multiprocessing
import os
import re
import spacy
from collections import defaultdict
from datetime import datetime

import config
import aiomysql
import pymysql

WIKI_DIR = "../corpora/wikiextractor/"
DEG_ASSOCIATION = 2
total_lines = 109579737


def reset_db(db):
    """ mainly for testing"""
    cursor = db.cursor()
    cursor.execute("DELETE FROM pos")
    cursor.execute("ALTER TABLE pos AUTO_INCREMENT = 1")
    pos = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
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

def update_pos(word_cache, cursor, pos): ###
    update = "UPDATE pos_list SET freq = freq + %s WHERE pos_id=%s AND word_id=%s"
    insert = "INSERT INTO pos_list (pos_id, word_id, freq) VALUES (%s, %s, %s)"
    commands = dict()
    commands[update] = []
    commands[insert] = []
    for word, pos_info in pos.items():
        id = word_cache[word]
        for pos, count in pos_info.items():
            posid = ns.pos.index(pos) + 1
            is_in = cursor.execute('SELECT * FROM pos_list WHERE word_id=%s AND pos_id=%s', (id, posid))
            if (not bool(is_in)):
                try:
                    cursor.execute(insert, (posid, id, 0))
                except pymysql.err.IntegrityError as e:
                    pass # it's in, just update it
            commands[update].append((count, posid, id))   
    cursor.executemany(update, commands[update])
    
def update_db(frequencies, pairings, pos, filename): ###
    max_tries = 10
    tries = 0;
    while tries < max_tries:
        try:
            """Async-ily updates the databaase"""
            word_cache = dict()
            commands = []
            db = pymysql.connect(host='localhost',
                                     user=config.sql_username,
                                     password=config.sql_pw,
                                     db=config.sql_db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            for word in frequencies:
                is_in_db = cursor.execute('SELECT id FROM words WHERE word=%s', (word,))
                if (is_in_db == 0):
                    cursor.execute('INSERT INTO words (id, word, freq) VALUES (null, %s, %s)', (word, frequencies[word]))
                    cursor.execute('SELECT id FROM words WHERE word=%s', (word,))
                    word_id = cursor.fetchone()
                    word_id = word_id["id"]
                else:
                    cursor.execute('SELECT id FROM words WHERE word=%s', (word,))
                    word_id = cursor.fetchone()
                    word_id = word_id["id"]
                word_cache[word] = word_id
            update_pairings(word_cache, db.cursor(), pairings)
            update_pos(word_cache, db.cursor(), pos)
            db.commit()
            tries = max_tries
        except pymysql.err.OperationalError as e:
            tries += 1 #deadlock, try again
            if tries == max_tries:
                print("!!! retry {} !!!".format(filename))




def read_data(file_name): ###
    """ Processes a file """
    lines = []
    pairings = defaultdict(int)
    frequencies = defaultdict(int)
    parts_of_speech = defaultdict(lambda: defaultdict(int))
    
    with open(file_name) as file:
        lines = file.readlines()
    print("READ      {} {}".format(file_name, now()))
    for line in lines:
        pa, fq, pos = extract_data(line.replace('"', ""))
        if pa != 0: # html line
            for word, count in fq.items():
                frequencies[word] += count
            for pairing, count in pa.items():
                pairings[pairing] += count
            for word, pos_count in pos.items():
                for pos, count in pos_count.items():
                    parts_of_speech[word][pos] += count
    print("PROCESSED {} {}".format(file_name, now()))
    update_db(frequencies, pairings, parts_of_speech, file_name)
    print("UPLOADED  {} {}".format(file_name, now()))
    ns.read += len(lines)
    print("{}% done".format(ns.read / ns.total_lines))

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
    pairings = {(word1, word2): count}
    frequencies = {word: count}
    words_pos = {word: {pos: count}}
    """
    space = spacy.load("en")
    if line == "" or line[0] == "<": return [0,0,0]
    pairings = defaultdict(int)
    frequencies = defaultdict(int)
    words_pos = defaultdict(lambda: defaultdict(int))
    line = space(line)
    for token in line: 
        if do_index(token):
            words_pos[token.text.lower()][token.pos_] += 1
            frequencies[token.text.lower()] += 1
    cap = len(line)
    for ti in range(cap):
        if do_index(line[ti]):
            lower = ti if ti < ns.degree else ns.degree
            upper = cap - ti -1 if ti >= cap - ns.degree -1 else ns.degree
            # the -1 is because (range(1, 1) won't run once for 1
            for i in range(lower):
                if do_index(line[ti-i-1]):
                    pairings[(line[ti-i-1].text.lower(), line[ti].text.lower())] += 1
            for i in range(upper):
                if do_index(line[ti+i+1]):
                    pairings[(line[ti].text.lower(), line[ti+i+1].text.lower())] += 1           
    return [pairings, frequencies, words_pos]


if __name__ == "__main__":

    db = pymysql.connect(host='localhost',
        user=config.sql_username,
        password=config.sql_pw,
        db=config.sql_db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    reset_db(db)
    db.close()

    # assigns globals to shared namespace
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.read = 0
    ns.pos = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
    ns.degree = DEG_ASSOCIATION
    ns.total_lines = total_lines

    # assume db is made

    # gets list of files to work through
    abspath = os.path.abspath(WIKI_DIR)
    files = []
    
    for f1 in os.listdir(WIKI_DIR):
        f1path = os.path.join(abspath, f1)
        if (os.path.isdir(f1path)):
            for f in os.listdir(os.path.join(abspath, f1)):
                fpath = os.path.join(f1path, f)
                if not (os.path.isdir(fpath)):
                    files.append(fpath)
    #files = ["../corpora/test0.txt", "../corpora/test1.txt", "../corpora/test2.txt"] * 9
    # test len is ~1800 lines
    

    # print(multiprocessing.cpu_count()) #4
    num_processes = 3
    chunksize = int(len(files) / num_processes)
    pool = multiprocessing.Pool(num_processes)
    
    results = pool.imap_unordered(read_data, files, chunksize)
    for r in results: 
        pass
    print("done")