import os
import re

def initialize(rootpath : str):
    
    # Get the list of filepaths from rootpath
    return __get_filepaths(rootpath)


def __get_filepaths(rootpath : str):
    
    # Initialize list to return
    filepaths = list()
    print(rootpath)
    
    # Recursively search the rootpath directory
    for dirpath, _, fpaths in os.walk(rootpath):
        
        # Iterate over each filename
        for fpath in fpaths:
            
            # Continue if file extension is not fortran
            extension = os.path.splitext(fpath)[1]
            if re.search("\.[fF][0-9]*$", extension) is None: continue
            
            # Add the complete filepath to the list to return
            filepath = os.path.join(dirpath, fpath)
            filepaths.append(str(filepath))

    return filepaths