import os
import spacy
import aiosqlite
from collections import defaultdict
import re
import asyncio
import timeit

DEFAULT_DB = "wikiInhaler.db"
WIKI_DIR = "../corpora/wikiextractor/"
DEG_ASSOCIATION = 2
SPACY_EN = spacy.load("en") 
read = 0
total = 109579737
make = True
make_commands = [ 
"""CREATE TABLE `words` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `word` TEXT NOT NULL UNIQUE, `wcount` INTEGER NOT NULL )""", 
"""CREATE TABLE "pairings" ( `word1id` INTEGER NOT NULL, `word2id` INTEGER NOT NULL, `count` INTEGER, PRIMARY KEY(`word1id`,`word2id`) )""",
"""CREATE TABLE "pos" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `pos` )""",
"""CREATE TABLE "pos_list" ( `posid` INTEGER NOT NULL, `wordid` INTEGER NOT NULL, `count` INTEGER NOT NULL, PRIMARY KEY(`posid`, `wordid`) )""",
]

update_word = "UPDATE words SET wcount = wcount + ? WHERE word=?"
insert_word = "INSERT INTO words (id, word, wcount) VALUES (null, ?, ?)"
upsert_word = """INSERT OR IGNORE INTO words (id, word, wcount) VALUES (null, ?, ?); UPDATE words SET wcount = wcount + ? WHERE word LIKE ?;"""
#//update_pairings = "UPDATE pairings SET count = count + ? WHERE word1id=? AND word2id=?"
#//insert_pairings = "INSERT INTO pairings (word1id, word2id, count) VALUES (?, ?, ?)"


async def update_db_word(word, count, db):
    cursor = await db.execute('SELECT * FROM words WHERE word=?', [word])
    if bool(await cursor.fetchone()):
        await db.execute(update_word, [count, word])
    else:
        await db.execute(insert_word, [word, count])


async def setup_table(db):
    global make
    if make:
        make = False
        for c in make_commands:
            await db.execute(c)
        #pos = [] # GET POS
        #db.executemany("INSERT INTO pos (id, pos) VALUES (null, ?)", pos)

def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return re.match(r".*[a-zA-Z]", s) and not re.match(r"[\d-]+", s)

# iteration one only get words and pos_list
async def read_data(file_name):
    global read
    global WORDS
    """
    async with aiosqlite.connect(...) as db:
        await db.execute('INSERT INTO some_table ...')
    await db.commit()

    async with db.execute('SELECT * FROM some_table') as cursor:
        async for row in cursor:
    """
    words = []
    lines = []
    pairings = {}
    fq = {}
    pos = {}
    frequencies = defaultdict(int)

    with open(file_name) as file:
        lines = file.readlines()

    for line in lines:
        pa, fq, pos = await extract_data(line.replace('"', ""))
        if pa != 0:
            for w, c in fq.items():
                frequencies[w] += c

    async with aiosqlite.connect(DEFAULT_DB) as db:
        await setup_table(db)   
        for w, c in frequencies.items():
            await update_db_word(w, c, db)

        await db.commit()
    read += len(lines)
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

async def tokenize(line):
    return SPACY_EN(line)

async def extract_data(line):
    if line == "" or line[0] == "<": return [0,0,0]
    pairings = defaultdict(int)
    frequencies = defaultdict(int)
    words_pos = defaultdict(int)
    line = await tokenize(line)
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
    #start = timeit.default_timer()
    """
    test = "AA/wiki_00"

    """
    loop = asyncio.get_event_loop()

    paths = []
    abspath = os.path.abspath(WIKI_DIR)
    lines = 0
    for f1 in os.listdir(WIKI_DIR):
        f1path = os.path.join(abspath, f1)
        if (os.path.isdir(f1path)):
            for f in os.listdir(os.path.join(abspath, f1)):
                fpath = os.path.join(f1path, f)
                if not (os.path.isdir(fpath)):
                    loop.run_until_complete(read_data(fpath))
                    #paths.append(fpath)
                    #loop.create_task(read_data(fpath))
                    #file = open(os.path.join(abspath, f1, f), errors='ignore')
                    #lines += len(file.readlines())
                    #file.close()

    #tasks = [loop.create_task(read_data(t)) for t in paths]
    #loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    #stop = timeit.default_timer()
    #print('Time: ', stop - start)  
    #40s
    #38s


