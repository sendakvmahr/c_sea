import os
import spacy
import sqlite3
from collections import defaultdict

DEFAULT_DB = "wikiInhaler.db"
WIKI_DIR = "../corpora/wikiextractor/"
DEG_ASSOCIATION = 2
SPACY_EN = spacy.load("en") 
DB = sqlite3.connect("text.db")
CURSOR = DB.cursor()
make = True
make_commands = [ 
"""CREATE TABLE `words` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `word` TEXT NOT NULL, `count` INTEGER NOT NULL )""", 
"""CREATE TABLE "pairings" ( `word1id` INTEGER NOT NULL, `word2id` INTEGER NOT NULL, `count` INTEGER, PRIMARY KEY(`word2id`,`word1id`) )"""
]

def read_data(file_name):
	if make:
		for c in make_commands:
			CURSOR.execute(c)
	lines = []
	with open(file_name) as file:
		lines = file.readlines()
	#counter = 0
	for line in lines:
		#counter+=1
		#if counter >= 5:
		#	return
		#print("---")
		print(line)
		pairings, frequencies, pos = extract_data(line.replace('"', ""))
		commands = []
		# MERGE BETWEEN LINES AND ONLY SHIP TO DB WHEN DONE PER FILE
		if pairings != 0:
			for word, count in frequencies.items():
				if is_in_word(word):
					commands.append(["UPDATE words SET count = count + ? WHERE word=?", (count, word)])
				else:
					commands.append(["INSERT INTO words (id, word, count) VALUES (null, ?, ?)", (word, count)])
			for c in commands:
				try:
					CURSOR.execute(c[0], c[1])
				except: 
					print(c)
					raise TypeError
			DB.commit()
			commands = []
			for pairing, count in pairings.items():
				ids = get_ids(pairing)
				if is_in_pairing(ids):
					commands.append(["INSERT INTO pairings (word1id, word2id, count) VALUES (?, ?, ?)", (ids[0], ids[1], count)])
				else:
					commands.append(["UPDATE pairings SET count = count + ? WHERE word1id=? AND word2id=?", (count, ids[0], ids[1])])
			for c in commands:
				try:
					CURSOR.execute(c[0], c[1])
				except: 
					print(c)
					raise TypeError



def get_ids(pair):
	id0 = CURSOR.execute('SELECT * FROM words WHERE word="{}"'.format(pair[0])).fetchone()[0]
	id1 = CURSOR.execute('SELECT * FROM words WHERE word="{}"'.format(pair[1])).fetchone()[0]
	return (id0, id1)

def is_in_pairing(ids):
    CURSOR.execute('SELECT * FROM pairings WHERE word1id=? AND word2id=?', (ids[0], ids[1]))

def is_in_word(word):
    CURSOR.execute('SELECT * FROM words WHERE word=?', (word,))
    return bool(CURSOR.fetchone())

def extract_data(line):
	if line == "" or line[0] == "<": return [0,0,0]
	pairings = defaultdict(int)
	frequencies = defaultdict(int)
	words_pos = defaultdict(int)
	line = SPACY_EN(line)
	for token in line: 
		if token.pos_ != "PROPN":
			words_pos[token.text.lower()] += 1
			frequencies[token.text.lower()] += 1
	cap = len(line)
	for ti in range(cap):
		if line[ti].pos_ != "PROPN":
			lower = ti if ti < DEG_ASSOCIATION else DEG_ASSOCIATION
			upper = cap - ti -1 if ti >= cap - DEG_ASSOCIATION -1 else DEG_ASSOCIATION
			# the -1 is because (range(1, 1) won't run once for 1
			for i in range(lower):
				if line[ti-i-1].pos_ != "PROPN":
					pairings[(line[ti-i-1].text.lower(), line[ti].text.lower())] += 1
			for i in range(upper):
				if line[ti+i+1].pos_ != "PROPN":
					pairings[(line[ti].text.lower(), line[ti+i+1].text.lower())] += 1 			
	return [pairings, frequencies, words_pos]


if __name__ == "__main__":
	test = "AA/wiki_00"
	read_data(WIKI_DIR + test)
	"""
	for f in os.listdir(WIKI_DIR):
	read_data(f)
	"""