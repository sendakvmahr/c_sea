import text.taggers.random_tagger
import text.tokenizers.basic_tokenizer

TAGGER = text.taggers.random_tagger.Random_Tagger()
TOKENIZER = text.tokenizers.basic_tokenizer.Basic_Tokenizer()

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
        t = "This is a sample of a text sentence."
        c_sea.read_text(t)
        t = input("input text:")
        c_sea.read_text(t)




