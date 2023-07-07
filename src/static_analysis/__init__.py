from static_analysis.parsing import Parser
from static_analysis.resolution import Resolver

class StaticAnalyzer:
    
    def __init__(self, specifications):
        self.specifications = specifications

    def run(self):
        """
        Finding the similar subprograms between each implementation, as well as the external variables and subprograms that are referenced by each.
        :implementations: List of objects representing each implementation.
        """
        
        # Parsing phase
        rootpaths = self.specifications.rootpaths
        filepaths = self.specifications.filepaths
        parser = Parser(rootpaths, filepaths)
        implementations = parser.run()
        
        # Resolution phase
        resolver = Resolver(implementations)
        implementations = resolver.run()
        
        return implementations