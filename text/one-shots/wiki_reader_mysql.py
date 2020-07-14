import multiprocessing
import os
import re
import spacy
import asyncio
from collections import defaultdict
from datetime import datetime

import config
import pymysql

connection = pymysql.connect(host='localhost',
                             user=config.sql_username,
                             password=config.sql_pw,
                             db=config.sql_db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print(connection)

def refresh_pos(db):
	db = connection.cursor()
    pos = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
	sql = "INSERT INTO `pos` (`id`, `pos`) VALUES (%s, %s)"
    for p in range(len(pos)):
		refresh_pos.execute(sql, (p+1, pos[p]))
    db.commit()

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

async def update_pairings(word_cache, cursor, pairings): ###
    update = "UPDATE pairings SET freq = freq + ? WHERE word1id=? AND word2id=?"
    insert = "INSERT INTO pairings (word1id, word2id, freq) VALUES (?, ?, ?)"
    commands = dict()
    commands[update] = []
    commands[insert] = []
    for pairing, count in pairings.items():
        ids = (word_cache[pairing[0]], word_cache[pairing[1]])
        await cursor.execute('SELECT * FROM pairings WHERE word1id=? AND word2id=?', ids)
        is_in = await cursor.fetchone()
        if (not bool(is_in)):
            try:
                await cursor.execute(insert, (ids[0], ids[1], 0))
            except sqlite3.IntegrityError:
                pass
        commands[update].append((count, ids[0], ids[1]))
    await cursor.executemany(update, commands[update])

async def update_pos(word_cache, cursor, pos): ###
    update = "UPDATE pos_list SET freq = freq + ? WHERE posid=? AND wordid=?"
    insert = "INSERT INTO pos_list (posid, wordid, freq) VALUES (?, ?, ?)"
    commands = dict()
    commands[update] = []
    commands[insert] = []
    for word, pos_info in pos.items():
        id = word_cache[word]
        for pos, count in pos_info.items():
            posid = ns.pos.index(pos) + 1
            await cursor.execute('SELECT * FROM pos_list WHERE wordid=? AND posid=?', (id, posid))
            is_in = await cursor.fetchone()
            if (not bool(is_in)):
                try:
                    await cursor.execute(insert, (posid, id, 0))
                except sqlite3.IntegrityError:
                    pass
            commands[update].append((count, posid, id))   
    await cursor.executemany(update, commands[update])
    
async def update_db(db_name, frequencies, pairings, pos): ###
    """Async-ily updates the databaase"""
    word_cache = dict()
    commands = []
    db = await aiosqlite.connect(db_name)
    cursor = await db.cursor()
    for word in frequencies:
        await cursor.execute('SELECT id FROM words WHERE word=?', (word,))
        fetch = await cursor.fetchone()
        if (fetch != None):
            await cursor.execute('INSERT INTO words (id, word, freq) VALUES (null, ?, ?)', (word, frequencies[word]))
            await cursor.execute('SELECT id FROM words WHERE word=?', (word,))
            id = await cursor.fetchone()[0]
        else:
            id = word[0]
            await cursor.execute('UPDATE words SET freq = freq + ? WHERE word=?', (frequencies[word], word))
        word_cache[word] = id
    await db.commit()
    await update_pairings(word_cache, await db.cursor(), pairings)
    db.commit()
    await update_pos(word_cache, await db.cursor(), pos)
    db.commit()

def read_data(file_name): ###
    """ Processes a file """
    lines = []
    pairings = defaultdict(int)
    frequencies = defaultdict(int)
    parts_of_speech = defaultdict(lambda: defaultdict(int))
    
    with open(file_name) as file:
        lines = file.readlines()
    print("READ {} {}".format(file_name, now()))
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_db(ns.db, frequencies, pairings, parts_of_speech))
    loop.close()
    print("UPLOADED {} {}".format(file_name, now()))
    ns.read += len(lines)
    return ns.read / ns.total_lines

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

def extract_data(line): ###
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
    #test = "AA/wiki_00"
    #read_data(WIKI_DIR + test)

    # assigns globals to shared namespace
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.read = 0
    ns.pos = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
    ns.degree = DEG_ASSOCIATION
    ns.db = DEFAULT_DB
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
    
    
    # print(multiprocessing.cpu_count()) #4
    num_processes = 3
    chunksize = int(len(files) / num_processes)
    pool = multiprocessing.Pool(num_processes)
    
    results = pool.imap_unordered(read_data, files, chunksize)
    for r in results: 
        print(r)