from utilities.types import Implementation, SourceFile
from static_analysis.parsing.tree_traversal import ParseTree

class Parser:
    
    def __init__(self, rootpaths : list[str], filepaths : list[list[str]]):
        """
        Initialize Parser object.
        :rootpaths: List of filepaths to each implementation source directory.
        :filepaths: List of lists of filepaths to each implementation source file, relative to its rootpath.
        """
        self.rootpaths = rootpaths
        self.filepaths = filepaths
    
    def run(self) -> list[Implementation]:
        """
        Parse the abstract structure of each implementation from the Flang parse tree of each of its source files.
        :rvalue: List of objects representing each implementation.
        """
        
        # List of implementations to return
        implems = []
        
        # Iterate over the indices associated with each implementation
        for implem_index in range(len(self.rootpaths)):
            
            # Unpack rootpath and filepaths for implementation
            implem_rootpath = self.rootpaths[implem_index]
            implem_filepaths = self.filepaths[implem_index]
            
            # Create new object representing implementation
            implem = Implementation()
            implems.append(implem)
            implem.filepath = implem_rootpath

            # Iterate over each filepath
            for filepath in implem_filepaths:
                
                # Get the filepath to the source file
                source_filepath = implem_rootpath + '/' + filepath
                
                # Create new object representing source file
                source = SourceFile()
                implem.sources.append(source)
                source.filepath = filepath
                
                # Generate the parse tree for source file
                tree = ParseTree(source_filepath)
                
                # Parse information about the program units in the source file
                source.programunits = tree.parse()
                    
        return implems