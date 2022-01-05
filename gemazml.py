"""
gemazml -- GEophysical MAgnetometry Zero Mean Line data processing software

This is a program designed to take magnetometer data and remove outliers, normalize
it to mean of zero, and write the results in a DAT file compatible with surfer.

Copyright (c) 2022 Autumn Bauman

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import argparse


def main():
    get_args()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="Input file path", type=str)
    parser.add_argument("outfile", help="Output file path", type=str)
    parser.add_argument(
        "-v", "--verbose", help="verbose output from program", action="store_true"
    )
    parser.add_argument(
        "-r",
        "--range",
        help="range of outliers to remove from data set. DEFAULT=100",
        type=float,
        nargs="?",
        const=100.0,
        default=100.0,
    )
    arguments = ["", "", False, 100]
    args = parser.parse_args()
    arguments[0] = args.infile
    arguments[1] = args.outfile
    if args.verbose:
        arguments[2] = True
    arguments[3] = args.range
    return arguments
