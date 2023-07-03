import sys
from initial.read_specifications import read_specifications
from information.tree_traversal import ParseTree


if __name__ == "__main__":

    # Get the .yaml file to parse from the command line arguments
    if len(sys.argv) == 2:
        yaml_filepath = sys.argv[1]
        tokens = yaml_filepath.split('/')
        yaml_directory = "." if len(tokens) == 1 else "/".join(tokens[:-1])
    else:
        raise Exception("Usage: python3 fortcompare.py [specifications-file]")

    # Read in the dictionary representation of the input .yaml file
    specs = read_specifications(yaml_filepath)

    # Get a list of the relative paths to source files
    sources = []
    for path in specs["source_paths"]:
        sources.append(yaml_directory + '/' + specs["source_root_path"] + '/' + path)

    # Get a list of the program units in all source files
    program_units = []
    for source in sources:
        tree = ParseTree(source)
        program_units.extend(tree.parse())
        
    # Print parsed program units
    for program_unit in program_units:
        print(str(program_unit))