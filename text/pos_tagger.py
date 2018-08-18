"""
Base class.
"""

class POS_Tagger():
    POS_TAGS = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
    
    def __init__(self):
        pass

    def tag(self):
        raise NotImplementedError("POS_Tagger.tag must be implemented in a child class.")

    def _int_to_pos(self, i):
        return POS_tagger.POS_TAGS[i]

    def _pos_to_int(self, pos):
        return POS_tagger.POS_TAGS.index(pos)

        
