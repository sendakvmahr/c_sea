from collections import defaultdict
import regex

TEST_PATH = "./corpora/UD_English-EWT/en_ewt-ud-train.conllu"


class CONLLU_Word():
    def __init__(self, text, lemma, pos, s_pos, attrs):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.stanford_pos = s_pos
        self.attrs = attrs

    def __str__(self):
        return "CONLLU_Word({})".format(self.text)

    def __repr__(self):
        return "CONLLU_Word({})".format(self.text)
    
    def indexed_text(self):
        if self.pos == "PROPN":
            return self.text
        return self.text.lower()
    
def read_file(path):
    result = []
    with open(path, "r", encoding="utf-8") as file:
        result = file.readlines()
    return result

def is_exclude(word):
    """
    #This is not training for errors, yet.
    exclude_regex = ["^!+$"]
    for r in exclude_regex:
        if re.match(r, word):
            return True
    return False
    """
    

def parse_attr(attrs):
    attrs = attrs.split("|")
    result = {}
    if attrs == ["_"]:
        return result
    for attr in attrs:
        typ, att = attr.split("=")
        result[typ] = att
    return result
        
def get_sentences(s):
    sents = []
    sentence = []
    for i in range(len(s)):
        if s[i][0] == "#":
            pass
        elif s[i][0] == "\n":
            sents.append(sentence)
            sentence = []
        else:
            word_def = s[i].split("\t")
            if is_exclude(word_def[1]):
                continue
            word = CONLLU_Word(word_def[1], word_def[2], word_def[3], word_def[4], parse_attr(word_def[5]))
            sentence.append(word)
    return sents

def append_pairs(pairs, words, sentence, window=2):
    sent_words = []
    for w in sentence:
        w_index = w.indexed_text()
        sent_words.append(w_index)
        words.add(w_index)
    for i in range(len(sent_words)):
        for r in range(1, window+1):
            if i+r <= len(sent_words)-1:
                pairs[(sent_words[i], sent_words[i+r])] += 1
            if i-r >= 0:
                pairs[(sent_words[i], sent_words[i-r])] += 1

contents = read_file(TEST_PATH)
sents = get_sentences(contents)
results = defaultdict(int)
words = set()

output_path = "./outputs/"

for i in range(len(sents)):
    append_pairs(results, words, sents[i])
    print("{}/{}".format(i, len(sents)))

words = sorted(list(words))

with open(output_path + "words.txt", "w", encoding="utf-8") as file:
    for item in words:
        file.write(item + "\n")

with open(output_path + "pairings.txt", "w", encoding="utf-8") as file:
    for key, count in list(results.items()):
        file.write("{} : {}\n".format(key, count))








      
