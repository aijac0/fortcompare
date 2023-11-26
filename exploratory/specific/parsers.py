from typing import Iterable
from abc import ABC, abstractmethod
import re

class Parser(Iterable, ABC):
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def __iter__(self) -> tuple[int, str]:
        pass
        

class StandardParser(Parser):
    
    def __init__(self, filepath : str):
        self.filepath = filepath 
        
    def __iter__(self) -> tuple[int, str]:
    
        # Open file
        f = open(self.filepath, 'r')      
        
        # Iterate over each line
        for line in f.readlines():
            
            # Get depth
            # Get identifier
            s = re.search('[^| ].*$', line)
            depth = int(s.start() / 2)
            identifier = s.group()
            yield depth, identifier
            
        # Close file
        f.close()