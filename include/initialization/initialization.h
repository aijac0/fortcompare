# ifndef INITIALIZATION_INITIALIZATION_H
# define INITIALIZATION_INITIALIZATION_H

# include <iostream>
# include <vector>
# include <filesystem>
# include <cstddef>

class InitializationData
{
    private :
        // Attributes
        std::vector< std::filesystem::path > rootpaths;                   // Paths to the root of each implementation source directory
        std::vector< std::vector< std::filesystem::path > > filepaths;    // Paths to source files in each implementation, relative to its rootpath
        
    public :
        // Constructor
        InitializationData(int n_filepaths)
            : rootpaths(n_filepaths),
            filepaths(n_filepaths) 
        {}

        // Friend class
        // This class will be the one that constructs it, destructs it, and can change its attributes
        friend class Initializer;

        // Friend functions
        // These functions will be able to access but not change its attributes
        // >> TODO
};

class Initializer
{
    private :
        // Attributes
        InitializationData data;

    public :
        // Constructor
        Initializer(int n_filepaths, char **c_filepaths);

        // Run
        InitializationData run();
};

# endif