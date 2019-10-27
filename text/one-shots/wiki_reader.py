import os
import spacy
import sqlite3
from collections import defaultdict
import re

DEFAULT_DB = "wikiInhaler.db"
WIKI_DIR = "../corpora/wikiextractor/"
DEG_ASSOCIATION = 2
SPACY_EN = spacy.load("en") 
DB = sqlite3.connect("text.db")
CURSOR = DB.cursor()
read = 0
total = 109579737
make = True
make_commands = [ 
"""CREATE TABLE `words` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `word` TEXT NOT NULL UNIQUE, `count` INTEGER NOT NULL )""", 
"""CREATE TABLE "pairings" ( `word1id` INTEGER NOT NULL, `word2id` INTEGER NOT NULL, `count` INTEGER, PRIMARY KEY(`word1id`,`word2id`) )""",
"""CREATE TABLE "pos" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `pos` )""",
"""CREATE TABLE "pos_list" ( `posid` INTEGER NOT NULL, `wordid` INTEGER NOT NULL, `count` INTEGER NOT NULL, PRIMARY KEY(`posid`, `wordid`) )""",
]

# iteration one only get words and pos_list
WORDS = set()
def read_data(file_name):
    global make
    if make:
        for c in make_commands:
            CURSOR.execute(c)
        pos = [] # GET POS
        CURSOR.executemany("INSERT INTO pos (id, pos) VALUES (null, ?)", pos)
        make = False
    update_word = "UPDATE words SET count = count + ? WHERE word=?"
    insert_word = "INSERT INTO words (id, word, count) VALUES (null, ?, ?)"
    word = """INSERT OR IGNORE INTO words (id, word, wcount) VALUES (null, ?, ?); UPDATE words SET wcount = wcount + ? WHERE word LIKE ?;"""
    #word="""INSERT INTO words(id,word,wcount) VALUES(null,?,?) ON CONFLICT(?) DO UPDATE SET wcount=wcount+?;"""
    #//update_pairings = "UPDATE pairings SET count = count + ? WHERE word1id=? AND word2id=?"
    #//insert_pairings = "INSERT INTO pairings (word1id, word2id, count) VALUES (?, ?, ?)"

    commands = defaultdict(list)

    global read
    global WORDS
    
    lines = []
    
    pairings = {}
    fq={}
    pos = {}
    frequencies = defaultdict(int)

    with open(file_name) as file:
        lines = file.readlines()
    
    for line in lines:
        read += 1
        
        pa, fq, pos = extract_data(line.replace('"', ""))
        # MERGE BETWEEN LINES AND ONLY SHIP TO DB WHEN DONE PER FILE oops
        if pa != 0:
            for w, c in fq.items():
                frequencies[w] += c
    for w, c in frequencies.items():
    	if w in WORDS:
        	commands[update_word].append([c, w])
    	else:
        	commands[insert_word].append([w, c])
        	WORDS.add(w)

    CURSOR.executemany(insert_word, commands[insert_word])
    CURSOR.executemany(update_word, commands[update_word])
    DB.commit()
    print(read/total)
    
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



def get_ids(pair):
    print(pair)
    id0 = CURSOR.execute('SELECT * FROM words WHERE word=?', (pair[0],)).fetchone()[0]
    id1 = CURSOR.execute('SELECT * FROM words WHERE word=?', (pair[1],)).fetchone()[0]
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
        return re.match(r".*[a-zA-Z]", s) and not re.match(r"[\d-]+", s)

def extract_data(line):
    if line == "" or line[0] == "<": return [0,0,0]
    pairings = defaultdict(int)
    frequencies = defaultdict(int)
    words_pos = defaultdict(int)
    line = SPACY_EN(line)
    for token in line: 
        if token.pos_ != "PROPN" and is_english(token.text):
            words_pos[token.text.lower()] += 1
            frequencies[token.text.lower()] += 1
    """
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
    """
    return [pairings, frequencies, words_pos]


if __name__ == "__main__":
    #test = "AA/wiki_00"
    #read_data(WIKI_DIR + test)
    abspath = os.path.abspath(WIKI_DIR)
    lines = 0
    for f1 in os.listdir(WIKI_DIR):
        f1path = os.path.join(abspath, f1)
        if (os.path.isdir(f1path)):
            for f in os.listdir(os.path.join(abspath, f1)):
                fpath = os.path.join(f1path, f)
                if not (os.path.isdir(fpath)):
                    read_data(fpath)
                    #file = open(os.path.join(abspath, f1, f), errors='ignore')
                    #lines += len(file.readlines())
                    #file.close()
    #print(lines)
    #109579737 lines
    DB.close()


