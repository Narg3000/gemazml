"""
gemazml -- GEophysical MAgnetometry Zero Mean Line data processing software

This is a program designed to take magnetometer data and remove outliers, normalize
it to mean of zero, and write the results in a DAT file compatible with surfer.



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

ARGUMENT PARSER - containes the get_param function
Takes no arguments and returns tuple.

Format of returned tuple:
order:      (infile, outfile, axis, range, time, sigma, verbose)
datatypes:  |str  | str   | str | float | bool| int  | bool   |
"""

# Argparse used to take input
import argparse


def getParameters(version):
    # set up the parameters
    parser = argparse.ArgumentParser(
        prog="gemazml",
        description="Processes magnetometry data to remove dropouts and normalize to a zero mean line",
    )
    # Optional Arguments!
    # Verbosity, not yet implemented well. If you use it rip stdout ig
    parser.add_argument(
        "-V", "--verbose", help="verbose output from program", action="store_true"
    )
    # Range, used for setting data range of intrest
    parser.add_argument(
        "-r",
        "--range",
        help="range of outliers to remove from data set. DEFAULT=100",
        type=float,
        nargs="?",
        default=100.0,
    )
    # -t --time: toggles runtime
    parser.add_argument(
        "-t",
        "--time",
        help="Toggels runtime logging, default false",
        action="store_true",
    )
    # multiple of sstandard deviations used to remove data outliers
    # in preprocessing
    parser.add_argument(
        "--destagger",
        help="Add an offset to every other scan row. Off by default",
        type=float,
        nargs="?",
        default=0
    )
    
    # Display version and copyright stuffs
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"gemazml version {version}. \n"
        + "(c) 2022 Autumn Bauman and Michael Rogers. \n licensed under the Apache 2.0 license",
    )

    subparsers = parser.add_subparsers(dest="mode")
    ####################################################################
    # FILE SECTION
    fileParse = subparsers.add_parser('file', help='Used for a single file')

    # Parser for file mode 

    fileParse.add_argument(
        "infile", help="Input file path",
        type=str
    )
    # Output File
    fileParse.add_argument("outfile", help="Output File Path", type=str)
    fileParse.add_argument(
        "axis", help="Axis along which data was gathered along",
        type=str,
        choices=['X', 'Y']
    )
    #######################################################################
    # Directory Section 
    # Parser for directories
    dirParser = subparsers.add_parser('dir', help="Used for directories of data")

    dirParser.add_argument(
        "infile", help="Input file path", type=str)
    dirParser.add_argument(
        "outfile", help="Directory to write to", type=str)
    dirParser.add_argument(
        "axis", help="Axis along which data was gathered along",
        type=str,
        choices=['X', 'Y']
    )
    # Turn input files into one big one on the output
    dirParser.add_argument("--append", help="append all files into single .dat. Default, false", action='store_true', default=False)
    # What extension to look for on the files 
    dirParser.add_argument("-e", "--extension", help="Extension on files. Default is '.dat'", type=str, default='.dat')



    

    args = parser.parse_args()
    # tuple to be returned
    return args
       