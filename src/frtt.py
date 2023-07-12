import sys
from initial import initial
from static_analysis import static_analysis

if __name__ == "__main__":

    # Get the .yaml file to parse from the command line arguments
    if len(sys.argv) == 3:
        rootpath1 = sys.argv[1]
        rootpath2 = sys.argv[2]
    else:
        raise Exception("Usage: python3 frtt.py source_directory_path_1 source_directory_path_2")

    # Run the initialization phase
    filepaths1, filepaths2 = initial(rootpath1, rootpath2)
    
    # Run the static analysis phase
    program1, program2, isomorphism = static_analysis(filepaths1, filepaths2)
    
    # Output result
    #print(str(program1))
    #print(str(program2))
    print(isomorphism)