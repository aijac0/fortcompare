import yaml

def read_specifications(filename):
    """
    Get the dictionary representation of the contents of a .yaml file.
    :filename: Name of the file, must have extension .yaml.
    :return: Dictionary containing the contents of the .yaml file.
    """

    # Read file into a dictionary
    f = open(filename, "r")
    specs = yaml.safe_load(f)
    f.close()
    return specs
