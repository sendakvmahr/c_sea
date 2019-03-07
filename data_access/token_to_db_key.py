import re as re

def is_english(s):
    """ Unicode hack that determines if there are any non-english
    characters used """
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
        
def is_not_number(s):
    sequence = re.compile("\d+")
    return not sequence.match(s)
    
def has_no_special(s):
    sequence = re.compile("^[a-zA-Z0-9]*$")
    return sequence.match(s)

def lowercase(s):
    return s.lower()
    
def remove_whitespace(s):
    return s.replace("\n", "").strip()

FILTER_FUNCTIONS = [has_no_special, is_not_number, is_english]
CONVERSION_FUNCTIONS = [lowercase, remove_whitespace]

class Token_To_DB_Key():
    def __init__(self, conversion_functions, filter_functions):
        self.conversion_functions = conversion_functions
        self.filter_functions = filter_functions
    
    def _check_eligible(self, token):
        is_eligible = True
        for f in self.filter_functions:
            is_eligible = is_eligible and f(token)
        return is_eligible
        
    def _convert(self, t):
        key = t
        for g in self.conversion_functions:
            key = g(key)
        return key
        
    def get_key(self, token):
        if type(token) == str:
            if self._check_eligible(token):
                return self._convert(token)
            else:
                return ""
        else: 
            if self._check_eligible(token.text):
                return self._convert(token.text)
            