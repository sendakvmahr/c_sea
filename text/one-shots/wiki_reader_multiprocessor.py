import aiosqlite
import multiprocessing
import os
import re
import spacy
import sqlite3
import asyncio
from collections import defaultdict

DEFAULT_DB = "wikiInhaler.db"
WIKI_DIR = "../corpora/wikiextractor/"
DEG_ASSOCIATION = 2
total = 109579737
make = True

def make_db():
    make_commands = [ 
    """CREATE TABLE `words` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `word` TEXT NOT NULL, `count` INTEGER NOT NULL )""", 
    """CREATE TABLE "pairings" ( `word1id` INTEGER NOT NULL, `word2id` INTEGER NOT NULL, `wcount` INTEGER, PRIMARY KEY(`word1id`,`word2id`) )""",
    """CREATE TABLE "pos" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `pos` TEXT NOT NULL )""",
    """CREATE TABLE "pos_list" ( `posid` INTEGER NOT NULL, `wordid` INTEGER NOT NULL, `wcount` INTEGER NOT NULL, PRIMARY KEY(`posid`, `wordid`) )""",
    ]
    db = sqlite3.connect(DEFAULT_DB)
    cursor = db.cursor()
    for c in make_commands:
        cursor.execute(c)
    pos = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
    pos = [(p,) for p in pos]
    cursor.executemany("INSERT INTO pos (id, pos) VALUES (null, ?)", pos)
    db.close()

async def get_pair_command(word_cache, word0, word1, count):
    update_word = "UPDATE words SET count = count + ? WHERE word=?"
    insert_word = "INSERT INTO words (id, word, count) VALUES (null, ?, ?)"
    word = """INSERT INTO words (id, word, count) VALUES (null, ?, ?)
    ON CONFLICT(word) DO UPDATE SET count = count + ?"""
    #id0 = word1 in word_cache ? word_cache[word1] : (CURSOR.execute('SELECT * FROM words WHERE word=?', (pair[0],)).fetchone()[0])
    #id1 = word1 in word_cache ? word_cache[word1] : (CURSOR.execute('SELECT * FROM words WHERE word=?', (pair[0],)).fetchone()[0])
    #actually what it should do is check 
    return 

async def update_db(db, frequencies, pairings, pos):
    word_cache = dict()
    # cache words in there
    # determine what maps to what for all the db options
    # execute them
    pass

def read_data(file_name):
    
    commands = defaultdict(list)
    lines = []
    
    pairings = {}
    fq = defaultdict(int)
    pos = {}
    
    with open(file_name) as file:
        lines = file.readlines()
    
    for line in lines:
        
        pa, fq, pos = extract_data(line.replace('"', ""))
        if pa != 0:
            for word, count in fq.items():
                frequencies[word] += count

    for word, count in frequencies.items():
        c[word].append(word, count, count)
    
    CURSOR.executemany(word, c[word])
    DB.commit()
        
    """
    if pairings != 0:
        for word, count in frequencies.items():
            if is_in_word(word):
                c[update_word].append((count, word))
            else:
                c[insert_word].append((word, count))
        CURSOR.executemany(insert_word, c[insert_word])
        CURSOR.executemany(update_word, c[update_word])
        DB.commit()
        for pairing, count in pairings.items():
            ids = get_ids(pairing)
            if is_in_pairing(ids):
                c[update_pairings].append((count, ids[0], ids[1]))
            else:
                c[insert_pairings].append((ids[0], ids[1], count))
        CURSOR.executemany(update_pairings, c[update_pairings])
        CURSOR.executemany(insert_pairings, c[insert_pairings])
    """
    ns.read += len(lines)
    return ns.read / 109579737



def get_ids(pair):
    print(pair)
    #id0 = CURSOR.execute('SELECT * FROM words WHERE word=?', (pair[0],)).fetchone()[0])
    #id1 = CURSOR.execute('SELECT * FROM words WHERE word=?', (pair[1],)).fetchone()[0])
    return (id0, id1)

def is_in_pairing(ids):
    CURSOR.execute('SELECT * FROM pairings WHERE word1id=? AND word2id=?', (ids[0], ids[1]))
    return bool(CURSOR.fetchone())

def is_in_word(word):
    return word in WORDS
    #CURSOR.execute('SELECT * FROM words WHERE word=?', (word,))
    #return bool(CURSOR.fetchone())

def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return re.match(r".*[a-zA-Z]", s)

def extract_data(line):
    if line == "" or line[0] == "<": return [0,0,0]
    pairings = defaultdict(int)
    frequencies = defaultdict(int)
    words_pos = defaultdict(int)
    line = ns.space(line)
    for token in line: 
        if token.pos_ != "PROPN" and is_english(token.text):
            words_pos[token.text.lower()] += 1
            frequencies[token.text.lower()] += 1
    cap = len(line)
    for ti in range(cap):
        if line[ti].pos_ != "PROPN" and is_english(token.text):
            lower = ti if ti < DEG_ASSOCIATION else DEG_ASSOCIATION
            upper = cap - ti -1 if ti >= cap - DEG_ASSOCIATION -1 else DEG_ASSOCIATION
            # the -1 is because (range(1, 1) won't run once for 1
            for i in range(lower):
                if line[ti-i-1].pos_ != "PROPN" and is_english(token.text):
                    pairings[(line[ti-i-1].text.lower(), line[ti].text.lower())] += 1
            for i in range(upper):
                if line[ti+i+1].pos_ != "PROPN" and is_english(token.text):
                    pairings[(line[ti].text.lower(), line[ti+i+1].text.lower())] += 1             
    return [pairings, frequencies, words_pos]


if __name__ == "__main__":
    #test = "AA/wiki_00"
    #read_data(WIKI_DIR + test)
    abspath = os.path.abspath(WIKI_DIR)
    lines = 0
    files = []
    
    for f1 in os.listdir(WIKI_DIR):
        f1path = os.path.join(abspath, f1)
        if (os.path.isdir(f1path)):
            for f in os.listdir(os.path.join(abspath, f1)):
                fpath = os.path.join(f1path, f)
                if not (os.path.isdir(fpath)):
                    files.append(fpath)
    
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.read = 0
    ns.space = spacy.load("en")
    make_db()
    
    
    # print(multiprocessing.cpu_count()) #4
    num_processes = 2
    chunksize = int(len(files) / num_processes)
    
    
    
    pool = multiprocessing.Pool(num_processes)
    
    results = pool.imap_unordered(read_data, files, chunksize)
    for r in results: 
        print(r)
                    #read_data(fpath)
                        
                    #file = open(os.path.join(abspath, f1, f), errors='ignore')
                    #lines += len(file.readlines())
                    #file.close()
    #print(lines)
    #109579737 lines

