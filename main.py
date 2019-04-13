import text.taggers.random_tagger
import text.tokenizers.basic_tokenizer
import data_access.db_wrapper
import data_access.token_to_db_key

TAGGER = text.taggers.random_tagger.Random_Tagger()
TOKENIZER = text.tokenizers.basic_tokenizer.Basic_Tokenizer()
CONVERTER = data_access.token_to_db_key.Token_To_DB_Key(data_access.token_to_db_key.CONVERSION_FUNCTIONS, data_access.token_to_db_key.FILTER_FUNCTIONS)
DB = data_access.db_wrapper.DB_Connection()

class Cerulean_Sea_Text():
	def __init__(self, tagger, tokenizer, converter, db):
		self.tagger = tagger
		self.tokenizer = tokenizer
		self.converter = converter
		self.db = db

	def read_text(self, text):
		text = "Here is some sample text. This is a very simple test case."
		print(text)
		tokens = self.tokenizer.tokenize(text)
		#print(tokens)
		tagged_tokens = self._analyze_tokens(tokens)
		#print(tagged_tokens)
		requests = [(self.converter.get_key(token), 1) for token in tagged_tokens]
		#print(requests)
		#for item in requests:
		#    self.db.add_item(item[0], item[1])
		#print(self.db.count())

	def _analyze_tokens(self, tokens):
		tagged_tokens = self._frequency_analyze(tokens)
		tagged_tokens = self.tagger.tag(tagged_tokens)
		return tagged_tokens

	def _frequency_analyze(self, tokens):
		print("{},{} - {},{}".format(tokens[0].text, tokens[1].text, tokens[0].text, tokens[2].text))
		print("{},{}-{},{}-{},{}".format(tokens[1].text, tokens[0].text, tokens[1].text, tokens[2].text, tokens[1].text, tokens[3].text))
		for i in range(2, len(tokens)-2):
			print("{},{} - {},{}".format(tokens[i].text, tokens[i+1].text, tokens[i].text, tokens[i+2].text))
				

if __name__ == "__main__":
	file = open("./text/corpora/test_xan_bie.txt", "r", encoding="utf-8")
	sample_text = file.read()
	file.close()
	c_sea = Cerulean_Sea_Text(TAGGER, TOKENIZER, CONVERTER, DB)
	while True:
		t = "This is a sample of a text sentence."
		t = sample_text
		c_sea.read_text(t)
		t = input("input text:")
		c_sea.read_text(t)




