import text.token

class Basic_Tokenizer():
	def __init__(self):
		pass
	def tokenize(self, to_parse):
		return [text.token.Token(t) for t in to_parse.split(" ")]