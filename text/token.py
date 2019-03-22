class Token():
    def __init__(self, text):
        self.text = text
        self.pos = ""
        
    def assign_pos(self, pos):
        self.pos = pos