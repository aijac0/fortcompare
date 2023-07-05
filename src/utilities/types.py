class Implementation:
    """
    Class that represents the abstract structure of a Fortran program implementation.
    """
    def __init__(self):
        self.filepath : str = None                  # Path to implementation root directory
        self.sources : list[SourceFile] = []        # List of source files in implementation
        
        
class SourceFile:
    """
    Class that represents the abstract structure of a Fortran source file.
    """
    def __init__(self):
        self.filepath : str = None                  # Path to source file
        self.programunits : list[SourceFile] = []   # List of program units in implementation


class ProgramUnit:
    """
    Class that represents the abstract structure of a Fortran program unit (module, subroutine, function).
    """
    def __init__(self):
        self.name : str = None                                        # Name of the program unit
        self.type : str = None                                        # Type of program unit ("module", "function", or "subroutine")
        self.referenced_modules : list[ProgramUnit] = list()          # List of modules referenced by program unit 
        self.declared_variables : list[Variable] = list()             # List of variables declared by program unit
        self.referenced_variables : list[Variable] = list()           # List of variables referenced by program unit
        self.referenced_programunits : list[ProgramUnit] = list()     # List of program units referenced by program unit (function or subroutine)
        # To be resolved into other attributes later:
        self.referenced_module_names : set[str] = set()               # Set of module names referenced by program unit
        self.referenced_names : set[str] = set()                      # Set of names referenced by program unit
        self.declared_names : set[str] = set()                        # Set of names declared by program unit
        
    def __str__(self):
        out_str = ""
        out_str += "ProgramUnit:\n"
        out_str += "\tName: " + self.name + "\n"
        out_str += "\tType: " + self.type + "\n"
        out_str += "\tReferenced Modules: " + ("\n" if self.referenced_modules else "None\n")
        for referenced_module in self.referenced_modules:
            out_str += "\t\t" + referenced_module + "\n"
        out_str += "\tDeclared Variables: " + ("\n" if self.declared_variables else "None\n")
        for declared_variable in self.declared_variables:
            out_str += "\t\t" + declared_variable + "\n"
        out_str += "\tReferenced Variables: " + ("\n" if self.referenced_variables else "None\n")
        for referenced_variable in self.referenced_variables:
            out_str += "\t\t" + referenced_variable + "\n"
        return out_str


class Variable:
    """
    Class that represents the abstract structure of a Fortran variable.
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
            