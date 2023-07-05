from static_analysis.parsing import Parser

class StaticAnalyzer:
    
    def __init__(self, specifications):
        self.specifications = specifications

    def analyze(self):
        """
        Finding the similar subprograms between each implementation, as well as the external variables and subprograms that are referenced by each.
        :implementation_sources: Dictionary mapping the name of each implementation to the relative paths to its source files.
        """
        
        # Parsing phase
        parser = Parser(self.specifications)
        information = parser.parse()
        
        return information