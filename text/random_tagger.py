from pos_tagger import POS_Tagger
from util import var
import random

class Random_Tagger(POS_Tagger):
    """If your POS tagger does worse than this class, it does not work."""
    def __init__(self):
        pass

    def tag(self, word):
        return random.choice(POS_Tagger.POS_TAGS)
