class Variable:
    """
    Class that can hold the necessary information about a Fortran variable.
    """
    
    def __init__(self):
        name : str = None
        type : str = None
        kind : int = None
        dimensions : list[int] = []
        attributes : list[str] = []
        assignment : str = None
        
    def is_valid(self):
        """
        Determine if a Variable represents a valid variable in Fortran.
        :self: Variable to validate
        :rvalue: True if 'self' is valid, False otherwise
        """
        
        if (self.name is None): return False
        if (self.type is None): return False
        if ("parameter" in self.attributes) ^ (self.assignment is None): return False
        return True
            