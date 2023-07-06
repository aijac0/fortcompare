# include <vector>
# include <filesystem>
# include <boost/algorithm/string.hpp>
# include "initialization/initialization.h"
# include <iostream>

/**
 * Constructor for the Initialization class.
 * :n_filepaths: Size of the c_filepaths array.
 * :c_filepaths: C string representations of the filepaths to each implementation source directory.
*/
Initialization::Initialization(int n_filepaths, char **c_filepaths)
: rootpaths(n_filepaths), filepaths(n_filepaths) 
{
    // Convert c_filepaths to its vector<path> representation
    for (int f = 0; f < n_filepaths; f++)
    {
        rootpaths[f] = c_filepaths[f];
    }

    // Get the paths to each Fortran source file relative to its implementation source directory
    // Iterate over each implementation source directory
    for (int r = 0; r < rootpaths.size(); r++)                                          
    {
        // Recursively traverse the implementation source directory
        for (auto &p : std::filesystem::recursive_directory_iterator(rootpaths[r]))
        {
            // Add relative filepath if it has a Fortran source file extension
            if (boost::algorithm::starts_with(p.path().extension().string(), ".f"))
            {
                filepaths[r].push_back(std::filesystem::relative(p.path(), rootpaths[r]));
            }
        }
    }
}