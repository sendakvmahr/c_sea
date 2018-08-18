from random_tagger import Random_Tagger
test_path = "./corpora/UD_English-EWT/en_ewt-ud-test.conllu"

with open(test_path) as file:
    for i in range(20):
        print(repr(file.readline()), end="\n")
