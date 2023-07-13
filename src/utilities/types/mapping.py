from __future__ import annotations
from typing import TypeVar, Generic

K = TypeVar('K')
V = TypeVar('V')

class Mapping(Generic[K, V]):
    
    def __init__(self):
        self.map : dict[K, V] = dict()            # Dictionary that represents a mapping
        self.domain : list[K] = list()            # Domain of the mapping
        
    def __getitem__(self, key : K) -> V:
        return self.map[key]
    
    def __setitem__(self, key : K, val : V):
        self.domain.append(key)
        self.map[key] = val
        
    def __iter__(self):
        return iter(self.domain)
    
    def __contains__(self, key : K) -> bool:
        return key in self.map
        
    def get(self, key : K) -> V:
        return self.map.get(key)
    
    @classmethod
    def invert(self) -> Mapping[V, K]:
        inverse = Mapping()
        for key in self:
            inverse[self[key]] = key
        return inverse