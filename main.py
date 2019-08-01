import text.taggers.random_tagger
import text.tokenizers.basic_tokenizer
import data_access.db_wrapper
import data_access.token_to_db_key

TAGGER = text.taggers.random_tagger.Random_Tagger()
TOKENIZER = text.tokenizers.basic_tokenizer.Basic_Tokenizer()
DB = data_access.db_wrapper.DB_Connection()
"""
because db should be tied into the conversion key, have the db connection object
be made with the wrapper, conversion formula, and the db itself

it should carry a cache/notepad for faster word lookup

"""

class Cerulean_Sea_Text():
        def __init__(self, tagger, tokenizer, db):
                self.tagger = tagger
                self.tokenizer = tokenizer
                self.db = db
                
        def _print_text(self):
                for t in self.tokens:
                        print(t)

        def record_text(self, text):
                text = "Here is some sample text. This is a very simple test case. Here is some sample text. This is a very simple test case."
                print(text)
                tokens = self.tokenizer.tokenize(text)
                tokens = self.tagger.tag(tokens)
                
                # "Optional" information to record
                tokens = self._frequency_analyze(tokens)
                
                for t in tokens:
                    self.db.increment(t)

                #self._print_text()
                #print(tagged_tokens)
                #requests = [(self.converter.get_key(), 1) for token in tagged_tokens]
                #print(requests)
                #for item in requests:
                #    self.db.add_item(item[0], item[1])
                #print(self.db.count())

        def _frequency_analyze(self, tokens):
                # doesn't count assign tokens to the last tw
                tokens[0].assign_adjacent(tokens[1].text)
                tokens[0].assign_adjacent(tokens[2].text)
                tokens[1].assign_adjacent(tokens[0].text)
                tokens[1].assign_adjacent(tokens[2].text)
                tokens[1].assign_adjacent(tokens[3].text)
                for i in range(2, len(tokens)-2):
                    tokens[i].assign_adjacent(tokens[i+2].text)
                    tokens[i].assign_adjacent(tokens[i+1].text)
                return tokens
                                

if __name__ == "__main__":
        file = open("./text/corpora/test.txt", "r")
        sample_text = file.read()
        file.close()
        c_sea = Cerulean_Sea_Text(TAGGER, TOKENIZER, DB)
        t="c"
        while t != "quit":
                t = "This is a sample of a text sentence."
                t = sample_text
                c_sea.record_text(t)
                t = input("input text:")
                c_sea.record_text(t)




