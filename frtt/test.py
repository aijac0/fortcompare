from initial.initialize import initialize
from static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree
import os


# Get source files
filepaths = initialize("codes")
ef = open("remove.txt", 'w')

# Iterate over each flang parse tree
for i in range(len(filepaths)):
    print("{} / {}".format(i+1, len(filepaths)))
    og_filepath = filepaths[i]
    filepath = og_filepath
    try:
        tree = get_abstract_syntax_tree(filepath, is_source=True)
        filepath = "data/raw" + filepath[len("codes"):]
        dirpath = "/".join(filepath.split("/")[:-1])
        if not os.path.exists("/".join(filepath.split("/")[:-1])):
            os.makedirs(dirpath)
        filepath = filepath.replace(".f90", ".txt")
        with open(filepath, 'w') as f:
            f.write(str(tree))
    except:
        ef.write(og_filepath + '\n')

ef.close()
    