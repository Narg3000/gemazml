"""
gemazml -- GEophysical MAgnetometry Zero Mean Line data processing software

This is a program designed to take magnetometer data and remove outliers, normalize
it to mean of zero, and write the results in a DAT file compatible with surfer.

v 0.0.0

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

# Function to deal with user input
def getParameters(version):
    # set up the parameters
    parser = argparse.ArgumentParser(
        prog="gemazml",
        description="Processes magnetometry data to remove dropouts and normalize to a zero mean line",
        usage="gemazml [INFILE] [OUTFILE] [AXIS] [options]",
    )
    # Positonal Arguments
    # input file path
    parser.add_argument("infile", help="Input file path", type=str)
    # output file path
    parser.add_argument("outfile", help="Output file path", type=str)
    # Axis along which data was gathered
    parser.add_argument(
        "axis",
        help="Axis data was gathered along. Accepts X or Y",
        type=str,
        choices=["X", "Y"],
    )
    # Optional Arguments!
    # Verbosity, not yet implemented
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
        "-S",
        "--sigma",
        type=int,
        help="Specify standard deviations from mean to remove data outliers in preprocessing. Default 20",
        nargs="?",
        default=20,
    )
    # Display version and copyright stuffs
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"gemazml version {version}. \n"
        + "(c) 2022 Autumn Bauman and CU Denver Physics dept.\n licensed under the Apache 2.0 license",
    )

    args = parser.parse_args()
    # tuple to be returned
    return (
        args.infile,
        args.outfile,
        args.axis,
        args.range,
        args.time,
        args.sigma,
        args.verbose,
    )
