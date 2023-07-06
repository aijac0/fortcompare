# ifndef INITIALIZATION_INITIALIZATION_H
# define INITIALIZATION_INITIALIZATION_H

# include <vector>
# include <filesystem>

/**
 * Class representation of the Initialization phase.
 * 
*/
class Initialization
{
    private :
        // Attributes
        std::vector< std::filesystem::path > rootpaths;                   // Paths to the root of each implementation source directory
        std::vector< std::vector< std::filesystem::path > > filepaths;    // Paths to source files in each implementation, relative to its rootpath
        
    public :
        // Constructor
        Initialization(int n_filepaths, char **c_filepaths);

        // Friend classes
        // These classes represent phases that use the results of this phases as input
        // >>> TODO
};

# endif