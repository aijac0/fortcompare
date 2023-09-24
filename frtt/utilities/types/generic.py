from typing import Union

class Program:
    """
    Class that represents the abstract structure of a Fortran program
    """
    def __init__(self):
        self.declared_programunits : list[ProgramUnit] = list()              # List of programunits in the program
        # Dictionaries that map names to objects
        self.declared_modules_map : dict[str, ProgramUnit] = dict()          # Dictionary that maps the name of a module to its object
        self.declared_procedures_map : dict[str, ProgramUnit] = dict()       # Dictionary that maps the name of a procedure to its object

        
    def __str__(self):
        out_str = ""
        for declared_programunit in self.declared_programunits:
            out_str += str(declared_programunit)
            out_str += "\n"
        return out_str


class ProgramUnit:
    """
    Class that represents the abstract structure of a Fortran program unit (module, subroutine, function).
    """
    def __init__(self):
        self.filepath : str = None                                             # Path to source file that contains the declaration for this program unit
        self.name : str = None                                                 # Name of the program unit
        self.type : str = None                                                 # Type of program unit ("module", "function", or "subroutine")
        self.referenced_modules : list[ProgramUnit] = list()                   # List of modules referenced by program unit 
        self.referenced_procedures : list[ProgramUnit] = list()                # List of procedures referenced by program unit
        self.referenced_variables : list[Variable] = list()                    # List of variables referenced by program unit
        self.declared_procedures : list[ProgramUnit] = list()                  # List of procedures declared by program unit
        self.declared_variables : list[Variable] = list()                      # List of variables declared by program unit
        self.parent : Union[Program, ProgramUnit] = None                       # Program or ProgramUnit for which the current program unit is a subprogram
        # To be resolved into other attributes later:
        self.referenced_module_names : set[str] = set()                        # Set of module names referenced by program unit
        self.referenced_procedure_names : set[str] = set()                     # Set of procedure names referenced by program unit
        self.referenced_names : set[str] = set()                               # Set of names referenced by program unit
        # Dictionaries that map names to objects
        self.declared_variables_map : dict[str, Variable] = dict()             # Dictionary that maps the name of a declared variable to its object
        self.declared_procedures_map : dict[str, ProgramUnit] = dict()         # Dictionary that maps the name of a procedure to its object
        
    def __str__(self):
        out_str = ""
        out_str += "ProgramUnit:\n"
        out_str += "\tName: " + self.name + "\n"
        out_str += "\tType: " + self.type + "\n"
        out_str += "\tReferenced Modules: " + ("\n" if self.referenced_modules else "None\n")
        for referenced_module in self.referenced_modules:
            out_str += "\t\t" + referenced_module.name + "\n"
        out_str += "\tReferenced Procedures: " + ("\n" if self.referenced_procedures else "None\n")
        for referenced_procedure in self.referenced_procedures:
            out_str += "\t\t" + referenced_procedure.name + "\n"
        out_str += "\tReferenced Variables: " + ("\n" if self.referenced_variables else "None\n")
        for referenced_variable in self.referenced_variables:
            out_str += "\t\t" + referenced_variable.name + "\n"
        out_str += "\tDeclared Procedures: " + ("\n" if self.referenced_procedures else "None\n")
        for declared_procedure in self.declared_procedures:
            out_str += "\t\t" + declared_procedure.name + "\n"
        out_str += "\tDeclared Variables: " + ("\n" if self.declared_variables else "None\n")
        for declared_variable in self.declared_variables:
            out_str += "\t\t" + declared_variable.name + "\n"
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