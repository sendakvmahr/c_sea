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
    
"""
import re as re

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
        self.cutoff = cutoff
        self.filter_functions = [is_english]


functions = [no_special, is_not_number, is_english]

k = ["one", "234", "!!!!", "Hello!"]

for i in k:
    for f in functions: 
        print(i, f(i))
