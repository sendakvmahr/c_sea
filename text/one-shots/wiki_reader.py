import os

WIKI_DIR = "../corpora/wikiextractor/"
DEG_ASSOCIATION = 2


for f in os.listdir(WIKI_DIR):
    read_data(f)

def read_data(file_name):
    lines = []
    with open(file_name) as file:
        lines = file.readlines()
    for line in lines:
        extract_data(line)
    # import db connection and send info here when done

def extract_data(lines):
    if line == "" or line[0] == "<": return
    """ run spacy on line, extract relevant information here"""
    
            
        



