# ifndef DATA_FILEPATHDATA_H
# define DATA_FILEPATHDATA_H

# include <vector>
# include <filesystem>

/**
 * Container for information about the filesystem location of source files in each implementation.
*/
class FilePathData
{
    public:
        // Attributes
        std::vector< std::filesystem::path > rootpaths;                   // Paths to the root of each implementation source directory
        std::vector< std::vector< std::filesystem::path > > filepaths;    // Paths to source files in each implementation, relative to its rootpath

        // Constructor
        FilePathData(int size) : rootpaths(size), filepaths(size) {}
};

# endif