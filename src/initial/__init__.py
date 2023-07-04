from yaml import safe_load

def initialize(specs_filepath):
    """
    Initialize the specifications dictionary.
    :specs_filepath: Path to .yaml file containing specifications
    :return: Dictionary representation of specifications.
    """
    
    # Read specifications file
    f = open(specs_filepath, "r")
    specs = safe_load(f)
    f.close()
    
    # Add entry containing filepath to specifications file
    tokens = specs_filepath.split('/')
    specs_directory = "." if len(tokens) == 1 else "/".join(tokens[:-1])
    specs["start_path"] = specs_directory
    
    return specs