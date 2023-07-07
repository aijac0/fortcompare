import sys
from initial import initialize
from static_analysis import StaticAnalyzer

if __name__ == "__main__":

    # Get the .yaml file to parse from the command line arguments
    if len(sys.argv) == 2:
        yaml_filepath = sys.argv[1]
    else:
        raise Exception("Usage: python3 frtt.py [specifications-file]")

    # Initialize the specifications dictionary
    specifications = initialize(yaml_filepath)
    
    # Run the static analysis phase
    static_analyzer = StaticAnalyzer(specifications)
    implementations = static_analyzer.run()
        
    # Output result
    for implem in implementations:
        for src in implem.sources.values():
            for punit in src.programunits.values():
                print("name : " + punit.name)
                print("type : " + punit.type)
                print("referenced_module_names: " + ("None" if not punit.referenced_module_names else ""))
                for name in punit.referenced_module_names:
                    print("\t" + name)
                print("referenced_names: " + ("None" if not punit.referenced_names else ""))
                for name in punit.referenced_names:
                    print("\t" + name)
                print("declared_names: " + ("None" if not punit.declared_names else ""))
                for name in punit.declared_names:
                    print("\t" + name)
                print()