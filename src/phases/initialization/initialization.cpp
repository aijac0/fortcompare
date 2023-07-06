# include <vector>
# include <filesystem>
# include <boost/algorithm/string.hpp>
# include "data/filepathdata.h"
# include "phases/initialization/initialization.h"

/**
 * Function representation of the initialization phase.
 * :n_filepaths: Size of the c_filepaths array.
 * :c_filepaths: C string representations of the filepaths to each implementation source directory.
 * :rvalue: Container for data about filesystem location of source files in each implementation.
*/
FilePathData* Initialization::run(int n_filepaths, char **c_filepaths)
{
    // Initialize return value
    FilePathData *fpath_data = new FilePathData(n_filepaths);

    // Convert c_filepaths to its vector<path> representation
    for (int f = 0; f < n_filepaths; f++)
    {
        fpath_data->rootpaths[f] = c_filepaths[f];
    }

    // Get the paths to each Fortran source file relative to its implementation source directory
    // Iterate over each implementation source directory
    for (int r = 0; r < fpath_data->rootpaths.size(); r++)                                          
    {
        // Recursively traverse the implementation source directory
        for (auto &p : std::filesystem::recursive_directory_iterator(fpath_data->rootpaths[r]))
        {
            // Add relative filepath if it has a Fortran source file extension
            if (boost::algorithm::starts_with(p.path().extension().string(), ".f"))
            {
                fpath_data->filepaths[r].push_back(std::filesystem::relative(p.path(), fpath_data->rootpaths[r]));
            }
        }
    }

    return fpath_data;
}