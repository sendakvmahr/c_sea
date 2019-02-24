import text.random_tagger
import text.basic_tokenizer

TAGGER = text.random_tagger.Random_Tagger()
TOKENIZER = text.basic_tokenizer.Basic_Tokenizer()

class Cerulean_Sea_Text():
	def __init__(self, tagger, tokenizer):
		self.tagger = tagger
		self.tokenizer = tokenizer

	def read_text(self, text):
		tokens = self.tokenizer.tokenize(text)
		print(tokens)
		tagged_tokens = self.tagger.tag(tokens)
		print(tagged_tokens)

if __name__ == "__main__":
	c_sea = Cerulean_Sea_Text(TAGGER, TOKENIZER)
	while True:
		t = input("input text:")
		c_sea.read_text(t)




