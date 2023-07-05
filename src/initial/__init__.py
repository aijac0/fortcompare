from yaml import safe_load
from utilities.types import Specifications

def initialize(specs_filepath):
    """
    Initialize the specifications dictionary.
    :specs_filepath: Path to .yaml file containing specifications
    :return: Dictionary representation of specifications.
    """
    
    # Read specifications file
    f = open(specs_filepath, "r")
    yaml_contents = safe_load(f)
    f.close()
    
    # Get path to directory containing specifications file
    tokens = specs_filepath.split('/')
    specs_directory = "." if len(tokens) == 1 else "/".join(tokens[:-1])
    
    # Create object representing specifications file
    specs = Specifications()
    specs.rootpaths = [specs_directory + '/' + implem["rootpath"] for implem in yaml_contents]
    specs.filepaths = [implem["filepaths"] for implem in yaml_contents]
    
    return specs