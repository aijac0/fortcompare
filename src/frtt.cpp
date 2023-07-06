# include <iostream>
# include "data/filepathdata.h"
# include "phases/initialization/initialization.h"

int main(int argc, char **argv)
{
    // Error check for command line arguments
    if (argc <= 1)
    {
        std::cerr << "Usage: frtt [initialization-file1] [initialization-file2] ..." << std::endl;
        return 1;
    }

    // Read command line args
    int n_filepaths = argc - 1;
    char **c_filepaths = argv + 1;

    // Initialization phase
    FilePathData *fpath_data = Initialization::run(n_filepaths, c_filepaths);

    // Static analysis phase
    // >>> TODO

    // Dynamic analysis phase
    // >>> TODO

    // Code generation phase
    // >>> TODO

    return 0;
}