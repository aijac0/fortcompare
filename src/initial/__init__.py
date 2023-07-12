import os
import fnmatch

def initial(rootpath1 : str, rootpath2 : str):
    
    # Get the list of filepaths from each rootpath
    filepaths1 = __get_filepaths(rootpath1)
    filepaths2 = __get_filepaths(rootpath2)

    return filepaths1, filepaths2


def __get_filepaths(rootpath : str):
    
    # Initialize list to return
    filepaths = list()
    
    # Recursively search the rootpath directory
    for dirpath, _, fpaths in os.walk(rootpath):
        
        # Iterate over each Fortran source filename
        for fpath in fnmatch.filter(fpaths, "*.f*"):
            
            # Add the complete filepath to the list to return
            filepath = os.path.join(dirpath, fpath)
            filepaths.append(str(filepath))

    return filepaths