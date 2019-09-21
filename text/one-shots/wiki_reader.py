import os
import spacy
import sqlite3
from collections import defaultdict

DEFAULT_DB = "wikiInhaler.db"
WIKI_DIR = "../corpora/wikiextractor/"
DEG_ASSOCIATION = 2
SPACY_EN = spacy.load("en") 


def read_data(file_name):
	lines = []
	with open(file_name) as file:
		lines = file.readlines()
	#counter = 0
	for line in lines:
		#counter+=1
		#if counter >= 5:
		#	return
		#print("---")
		print(extract_data(line))

	# import db connection and send info here when done

def extract_data(line):
	if line == "" or line[0] == "<": return
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