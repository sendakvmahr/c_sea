"""
if it's a BIG document, go chunk by chunk
if it's less than a chunk...
just take abit and go

then parse word by word while tallyingthings

for now, do it sentenec by sentence

then tally up word count IF

it's english
it's not all all numbers and spcial characters

and if the counts are above a cutoff


basic tokenizer should split on newlines
"""
import re as re
import tokenizers.basic_tokenizer as bt
import collections

def normalize_for_db(text):
    return text.lower().strip()

def is_english(s):
    """
    Unicode hack that determines if there are any non-english
    characters used
    """
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
        
def is_not_number(s):
    sequence = re.compile("\d+")
    return not sequence.match(s)
    
def no_special(s):
    sequence = re.compile("^[a-zA-Z0-9]*$")
    return sequence.match(s)
    
class Word_Reader():
    def __init__(self):
        self.cutoff = "cutoff"
        self.filter_functions = [is_english]
    def accept(self, word):
        return is_not_number(word) and no_special(word) and is_english(word)


with open("./corpora/test.txt", "r") as file:
    text = file.read()
    tokenizer = bt.Basic_Tokenizer()
    wr = Word_Reader()
    words = tokenizer.tokenize(text)
    words = [normalize_for_db(w) for w in words]
    result = collections.defaultdict(int)
    for w in words:
        if wr.accept(w):
            result[w] += 1
    print(result)
