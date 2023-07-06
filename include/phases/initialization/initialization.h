# ifndef INITIALIZATION_INITIALIZATION_H
# define INITIALIZATION_INITIALIZATION_H

# include <vector>
# include <filesystem>
# include "data/filepathdata.h"

/**
 * Class representation of the Initialization phase.
*/
class Initialization
{
    public :
        // Function representation of the phase.
        static FilePathData* run(int n_filepaths, char **c_filepaths);
};

# endif