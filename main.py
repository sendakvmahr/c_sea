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
        tokens = self.tokenizer.tokenize(text)
        print(tokens)
        tagged_tokens = self.tagger.tag(tokens)
        print(tagged_tokens)
        requests = [(self.converter.get_key(token[0]), 1) for token in tagged_tokens]
        print(requests)
        for item in requests:
            self.db.add_item(item[0], item[1])
        print(self.db.count())
        

if __name__ == "__main__":
    c_sea = Cerulean_Sea_Text(TAGGER, TOKENIZER, CONVERTER, DB)
    while True:
        t = "This is a sample of a text sentence."
        c_sea.read_text(t)
        t = input("input text:")
        c_sea.read_text(t)




