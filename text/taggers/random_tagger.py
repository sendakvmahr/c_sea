from text.taggers.pos_tagger import POS_Tagger
from util import _vars
import random

class Random_Tagger(POS_Tagger):
    """If your POS tagger does worse than this class, it does not work."""
    def __init__(self):
        pass

    def tag(self, words):
        result = []
        for w in words:
            w.assign_pos(random.choice(_vars.POS_TAGS))
            result.append(w)
        return result
