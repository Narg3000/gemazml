# gemazml
## A python utility to process magnetometry data

This program is still in the early days of its life so please let us know of any bugs that need fixing!

Basic usage:
```
python gemazml [INPUT FILEPATH] [OUTPUT FILEPATH] [AXIS] options
```
`INPUT FILEPATH` is the location of the file to be processed
`OUTPUT FILEPATH` The file to write output to. NOTE: WILL OVERWRITE EXISTING FILES
`AXIS` accepts `X` or `Y`. Which direction was the data taken along.
### Options
|Option | description|
|-------|------------|
|`-h --help` | Displays the help|
|`-v --version` | Displays version information |
|`-r [RANGE] --range [RANGE]` |   Sets the data range which is allowed. Values further than this from the mean will be removed from the dataset after normalization. DEFAULT: 100|
|`-t --time` | Logs the runtime of the program and outputs to the terminal |
|`-s --sigma` | How many standard deviations from the mean data can be. Datapoints outside of this range are removed. This is done before zero mean line normalization so the default value is very high, sigma = 20. |
|`-V --verbose` | Sets the terminal fillingness of the program |

### Usage and installation
This program is meant to be used from the command line, although hopefully a GUI will be coming soon... To use the program simply download the src folder, open up a terminal or command prompt window, and run:
```
python gemazml.py [INPUT FILEPATH] [OUTPUT FILEPATH] [AXIS] Options
```
An executable form is being worked on for Linux and Windows and a graphical frontend is on my list.

### Contact Info

For any questions or comments please email autumn.bauman@protonmail.com.

### That legal stuffs
Copyright (c) 2022 Autumn Bauman and Michael Rogers

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
