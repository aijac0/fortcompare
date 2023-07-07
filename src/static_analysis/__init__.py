from utilities.types import Specifications
from static_analysis.parsing import parse
from static_analysis.resolution import resolve

def statically_analyze(specifications : Specifications):
    """
    Finding the similar subprograms between each implementation, as well as the external variables and subprograms that are referenced by each.
    :implementations: List of objects representing each implementation.
    """
    
    # Run the parsing phase
    implementations = parse(specifications)
    
    # Run the resolution phase
    resolve(implementations)
    
    return implementations