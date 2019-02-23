import random_tagger

TAGGER = random_tagger.Random_Tagger()

class Cerulean_Sea_Text():
	def __init__(self, tagger, tokenizer):
		self.tagger = tagger

	def read_text(self, text):
		tokens = self.tokenizer.tokenize(text)
		tagged_tokens = self.tagger.tag(tokens)







if __name__ == "__main__":
	c_sea = Cerulean_Sea_Text()





