from collections import defaultdict

class Token():
    def __init__(self, text):
        self.text = text
        self.pos = ""
        self._adjacent = defaultdict(int)

    def assign_pos(self, pos):
        self.pos = pos

    def assign_adjacent(self, words):
    	if type(words) != str:
    		for word in words:
    			self._adjacent[word] += 1
    	else:
    		self._adjacent[words] += 1
            
            
    def __str__(self):
        return "Token(text='{}', pos='{}', _adjacent='{}')".format(self.text, self.pos, str(self._adjacent))
    
    def __repr__(self):
        return "Token(text='{}', pos='{}', _adjacent='{}')".format(self.text, self.pos, str(self._adjacent))
    
    