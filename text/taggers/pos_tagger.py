"""
Base class.
"""
from util import _vars

class POS_Tagger():
    
    def __init__(self):
        pass

    def tag(self):
        raise NotImplementedError("POS_Tagger.tag must be implemented in a child class.")

    def _int_to_pos(self, i):
        return POS_tagger.POS_TAGS[i]

    def _pos_to_int(self, pos):
        return POS_tagger.POS_TAGS.index(pos)

        
