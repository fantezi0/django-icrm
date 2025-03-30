class HashMapManager:
    def __init__(self):
        self.map = {}
        
    def register_item(self, item):
        first_letter = item.name[0]
        if first_letter not in self.map:
            self.map[first_letter] = []
        self.map[first_letter].append(item)
    
    def get_items(self, letter):
        return self.map.get(letter.lower(), [])    
    
    def rebuild(self, items):
        self.map.clear()
        for item in items:
            self.register_item(item)