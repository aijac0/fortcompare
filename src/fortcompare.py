import sys
from initial import initialize
from static_analysis import StaticAnalyzer

if __name__ == "__main__":

    # Get the .yaml file to parse from the command line arguments
    if len(sys.argv) == 2:
        yaml_filepath = sys.argv[1]
    else:
        raise Exception("Usage: python3 fortcompare.py [specifications-file]")

    # Initialize the specifications dictionary
    specifications = initialize(yaml_filepath)
    
    # Run the static analysis phase
    static_analyzer = StaticAnalyzer(specifications)
    information = static_analyzer.analyze()
        
    # Print parsed program units
    for implem_name, implem_info in information.items():
        for source_path, source_info in implem_info.items():
            for programunit_name, programunit in source_info.items():
                print(str(programunit))