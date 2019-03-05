""" testing db storage """

class DB_Connection():
    def __init__(self):
        self.db = set()
        
    def add_item(self, item, count):
        self.db.add(item)
    
    def count(self):
        return len(self.db)