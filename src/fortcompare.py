import sys
from initial import initialize
from information import gather_information


if __name__ == "__main__":

    # Get the .yaml file to parse from the command line arguments
    if len(sys.argv) == 2:
        yaml_filepath = sys.argv[1]
    else:
        raise Exception("Usage: python3 fortcompare.py [specifications-file]")

    # Initialize the specifications dictionary
    specs = initialize(yaml_filepath)
    
    # Gather information from source files
    information = gather_information(specs)
        
    # Print parsed program units
    for implem_name, implem_info in information.items():
        for source_path, source_info in implem_info.items():
            for programunit_name, programunit in source_info.items():
                print(str(programunit))