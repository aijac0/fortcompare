from abc import ABC, abstractmethod

class AbstractInput(ABC):
    
    @abstractmethod
    def serialize(dirpath, filename):
        pass
    
    @abstractmethod
    def deserialize(dirpath, filename):
        pass

class AbstractOutput:

    @abstractmethod
    def serialize(dirpath, filename):
        pass
        
    @abstractmethod
    def deserialize(dirpath, filename):
        pass