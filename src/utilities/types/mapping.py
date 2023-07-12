from collections import UserDict

class Mapping:
    
    def __init__(self):
        self.map = dict()               # Dictionary that represents a mapping
        self.domain = list()            # Domain of the mapping
        
    def __getitem__(self, key):
        return self.map[key]
    
    def __setitem__(self, key, val):
        self.domain.append(key)
        self.map[key] = val
        
    def __iter__(self):
        return iter(self.domain)
    
    def __contains__(self, key):
        return key in self.map
        
    def get(self, key):
        return self.map.get(key)
    
    def invert(self):
        inverse = Mapping()
        for key in self:
            inverse[self[key]] = key
            