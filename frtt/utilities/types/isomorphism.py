from frtt.utilities.types.mapping import Mapping
from frtt.utilities.types.generic import ProgramUnit, Variable


class Isomorphism:
    
    def __init__(self):
        programunit_map : Mapping[ProgramUnit, ProgramUnit] = Mapping()
        variable_map : Mapping[Variable, Variable] = Mapping()