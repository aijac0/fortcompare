import sys
from initial import initialize
from static_analysis import statically_analyze

if __name__ == "__main__":

    # Get the .yaml file to parse from the command line arguments
    if len(sys.argv) == 2:
        yaml_filepath = sys.argv[1]
    else:
        raise Exception("Usage: python3 frtt.py [specifications-file]")

    # Run the initialization phase
    specifications = initialize(yaml_filepath)
    
    # Run the static analysis phase
    implementations = statically_analyze(specifications)
        
    # Output result
    for implem in implementations:
        for src in implem.sources:
            for punit in src.programunits:
                print("name : " + punit.name)
                print("type : " + punit.type)
                print("referenced_modules: " + ("None" if not punit.referenced_modules else ""))
                for module in punit.referenced_modules:
                    print("\t" + module.name)
                print("declared_variables: " + ("None" if not punit.declared_variables else ""))
                for variable in punit.declared_variables:
                    print("\t" + variable.name)
                print("referenced_variables: " + ("None" if not punit.referenced_variables else ""))
                for variable in punit.referenced_variables:
                    print("\t" + variable.name)
                print("referenced_programunits: " + ("None" if not punit.referenced_programunits else ""))
                for programunit in punit.referenced_programunits:
                    print("\t" + programunit.name)
                print()