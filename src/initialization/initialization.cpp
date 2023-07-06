# include <filesystem>
# include <vector>
# include <string>
# include <boost/algorithm/string.hpp>
# include "initialization/initialization.h"

/**
 * Constructor for the Initializer class.
 * :n_filepaths: Size of the c_filepaths array.
 * :c_filepaths: C string representations of the filepaths to each implementation source directory.
*/
Initializer::Initializer(int n_filepaths, char **c_filepaths)
: data(n_filepaths)
{
    // Convert c_filepaths to its vector<path> representation
    for (int f = 0; f < n_filepaths; f++)
    {
        data.rootpaths[f] = c_filepaths[f];
    }
}


/**
 * Run the initialization phase.
*/
InitializationData Initializer::run()
{
    // Get the paths to each Fortran source file relative to its implementation source directory
    // Iterate over each implementation source directory
    for (int r = 0; r < data.rootpaths.size(); r++)                                          
    {
        // Recursively traverse the implementation source directory
        for (auto &p : std::filesystem::recursive_directory_iterator(data.rootpaths[r]))
        {
            // Add relative filepath if it has a Fortran source file extension
            if (boost::algorithm::starts_with(p.path().extension().string(), ".f"))
            {
                data.filepaths[r].push_back(std::filesystem::relative(p.path(), data.rootpaths[r]));
            }
        }
    }

    return data;
}