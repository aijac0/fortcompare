from utilities.types.mapping import Mapping
from utilities.types.generic import ProgramUnit, Variable


class Isomorphism:
    
    def __init__(self):
        programunit_map : Mapping[ProgramUnit, ProgramUnit] = Mapping()
        variable_map : Mapping[Variable, Variable] = Mapping()