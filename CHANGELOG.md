# Changelog of gemazml

### V 0.1.0; April 22 2022
Added Featured
  - `--destagger` option added
  - `file` and `dir` modes added
  - `-e --extension` options added to select which files are processed in directory mode
  - `--append` option added in dir mode to allow for the output to be concatenated into single file
  - Ability for itterating through directories implemented
Removed
  - `-s --sigma` options removed and a better way of removing outliers was added (limit by 20000nT < reading < 70000nT)

Changes:
  - redesigned the data reading in system to be all in pandas. hopefully will be faster
 
Bugs Fixed 
  - Enabeled use of non conditioned files
  - No longer prints out tab seperated values and is now fixed width. This simplifies working with surfer (hopefully)

### V 0.0.1; January 6 2022
Added Features:
  - `-v --version` and `-s --sigma` options added and implemented.
  - `-r --range` implemented as a step after zml processing to cutoff data outliers.

Changes:
  - changed return type of `getParameters` to tuple from list.
  - renamed `get_args` to `getParameters`
  
No bugs or removed features to be reprted

### V 0.0.0; January 5 2022
Added Features:
  - initial commit
  - Command arguments
  - started porting core functionality from jupyter notebook to standalone program

Removed Features:
  - Nothing, this is literally 0.0.0

Bugs Fixed:
  - Literally nothing this is 0.0.0
