from static_analysis.parsing.tree_traversal import ParseTree

class Parser:
    
    def __init__(self, specifications):
        self.specifications = specifications
    
    def parse(self):
        """
        Parsing phase.
        """
        
        # Initialize the dictionary to contain information
        info = dict()
        
        # Gather the information contained in each implementation
        for implem in self.specifications["implementations"]:
            
            # Unpack specifications about implementation
            implem_name = implem["name"]
            implem_root_path = implem["root_path"]
            
            # Add new entry to information dictionary
            info[implem_name] = dict()
            
            # Gather the information contained in each source file
            for source_path in self.specifications["source_paths"]:
                
                # Add new entry to information dictionary
                info[implem_name][source_path] = dict()
                
                # Get the full path to source file
                filepath = self.specifications["start_path"] + '/' + implem_root_path + '/' + source_path
                
                # Generate the parse tree for source file
                tree = ParseTree(filepath)
                
                # Parse information about the program units in the source file
                program_units = tree.parse()
                
                # Add an entry to the information dictionary for each program unit
                for program_unit in program_units:
                    info[implem_name][source_path][program_unit.name] = program_unit
                    
        return info