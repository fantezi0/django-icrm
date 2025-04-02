class HashMapManager:
    _hash_map = {}
    
    @classmethod
    def add_to_map(cls, item):
        if item not in cls._hash_map:
            cls._hash_map[item.name] = item
    @classmethod
    def get_from_map(cls, key):
        if key in cls._hash_map:
            return cls._hash_map[key]
        else:
            return None
        
    @classmethod
    def remove_from_map(cls, key):
        if key[0] in cls._hash_map:
            del cls._hash_map[key[0]][key]
            return True
        else:
            return False
        
    @classmethod
    def load_map(cls, items):
        for item in items:
            cls.add_to_map(item)
        
    @classmethod
    def clear_map(cls):
        cls._hash_map.clear()
        