from frtt.initial.initialize import initialize


def initial(rootpath1 : str, rootpath2 : str):
    
    # Get the list of filepaths from each rootpath
    filepaths1 = initialize(rootpath1)
    filepaths2 = initialize(rootpath2)

    return filepaths1, filepaths2