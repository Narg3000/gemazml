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

MAIN FILE
Contains main() and associated functions to drive the program

"""
from GetArgs import getParameters
import timeit
from gridprocessclass import Normalizer


def main():
    # VERSION NUMBER, TAKES STRING VALUE
    version = "0.0.0"
    # parse command input and store as the tuple args[]
    args = getParameters(version)
    verbose = args[6]
    # args[0] - infile
    # args[1] - outfile
    # args[2] - axis
    # args[3] - range
    # args[4] - time
    # args[5] - sigma
    # args[6] - verbosity, not yet used
    # args[7] - destagger, not yet implemented
    # -------------------------------------------
    # Initalise Normalizer objects
    totally_tubular = Normalizer(args[0], args[2], args[3])
    totally_tubular.DelOutliers(args[5], verbose)
    totally_tubular.ZmlInator()
    # Write the processed data to file
    totally_tubular.writeout(args[1], verbose)


main()
