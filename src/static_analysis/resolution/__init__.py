from utilities.types import Implementation, SourceFile

class Resolver:
    
    def __init__(self, implementations : list[Implementation]):
        """
        Initialize Parser object.
        :implementations: List of objects representing each implementation.
        """
        self.implementations = implementations
    
    def run(self) -> list[Implementation]:
        """
        Parse the abstract structure of each implementation from the Flang parse tree of each of its source files.
        :rvalue: List of objects representing each implementation.
        """
        
        # List of implementations to return
        implems = self.implementations
        
        # TODO
                    
        return implems