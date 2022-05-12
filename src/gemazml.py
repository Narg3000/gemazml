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

MAIN FILE
Contains main() and associated functions to drive the program

"""
from GetArgs import getParameters
import timeit
from gridprocessclass import Normalizer
import os
import datetime


def main():
    # VERSION NUMBER, TAKES STRING VALUE
    version = "0.1.0"

    # parse command input and store as the tuple args[]
    args = getParameters(version)
    verbose = args.verbose

    # ---------------------------------------
    # List of the argument positions
    # args.infile
    # args.outfile
    # args.axis
    # args.range
    # args.time
    # args.verbosity
    # args.destagger, not yet implemented
    # args.mode, file or dir modes
    # args.append, whether or not to append all the files into a single .dat from hell when in dir mode
    # -------------------------------------------
    # Initalise Normalizer objects

    if os.path.exists(args.infile) == False:
        raise Exception("Input path does not exist!")

    elif args.mode == "file":
        if os.path.isfile(args.infile) == False:
            raise Exception("Input file must be file! To operate on a directory use dir mode.")

        totally_tubular = Normalizer(args.infile, args.axis, args.range)
        # Below line is useful for debugging the fileIO module I wrote. Don't use it unless you are debugging please.
        # totally_tubular.writeout("initout.dat", verbose)
        # removes data thats too out there
        totally_tubular.DelOutliers(verbose)
        # Normalizes data to a zero mean line
        totally_tubular.ZmlInator()
        # Destagger the data
        if args.destagger:
            totally_tubular.destaggerer(args.destagger, verbose)
        # Remove outliers still present after normalization
        totally_tubular.limitRange()
        # Write the processed data to file
        totally_tubular.writeout(args.outfile, verbose)

    elif args.mode == "dir":
        # This is just all input protection to make sure the file system doesn't get fucked 
        outpath = args.outfile
        # First we see if the output location exists. If it does not and we are not in append mode it will be created.
        if (os.path.exists(outpath) == False) and (args.append == False):
            if args.outfile.endswith(args.extension) == False:
                os.makedirs(outpath)
            else: 
                raise Exception(f"Could not create output path, directory cannot end in {args.extension}!")

        if args.append and os.path.exists(outpath):
            n = outpath.rfind('.')
            i = 1
            outpathnew = outpath[:n] + str(i) + outpath[n:]
            while (os.path.exists(outpathnew))== True:
                i
                outpathnew = outpath[:n] + str(i) + outpath[n:]
            outpath = outpathnew
        
        if (os.path.isdir(outpath) == False) and (args.append == False):
            raise Exception("Output location must be directory! To concatonate output files use --append option")

        # Ensure a directory was passed for input
        if os.path.isdir(args.infile) == False:
            raise Exception("Input must be a directory, not a file. To operate on a file, use file mode.")

        # Lists out the files stored in input directories.
        basepath = args.infile # Makes coding easier and might reduce access times
        fileList = []
        ExtLength = int(-1 * len(args.extension))
        # This thing goes and makes the list of all the files I will be working with

        for files in os.listdir(basepath):
            if files.endswith(args.extension): # Boo! Scary inefficent and unpythonic code!
                if os.path.isfile(str(basepath + '/' + files)): #Whats worse is that I didn't punctuation right.
                    # This just stores the file path 
                    fileList.append(str(files[:ExtLength]))

        #------------------------------------------------------------------------------------------
        # This section is what does the processing 
        if verbose: print(f"processing files: \n {str(fileList)}")
        # this is the main loop which will run everything in the directory mode
        newfile = True
        for files in fileList:
            datSet = str(basepath + '/' + files + args.extension)
            anthony = Normalizer(datSet, args.axis, args.range)
            anthony.DelOutliers(verbose)
            anthony.ZmlInator()
            if args.destagger:
                anthony.destaggerer(args.destagger, verbose)
            anthony.limitRange()
            
            if args.append:
                if os.path.isdir(args.outfile):
                    raise Exception("When using append mode output file cannot be directory.")
                anthony.concatOut(outpath, verbose, newfile)
                newfile = False

            else:
                anthony.writeout(str(outpath + '/' + files + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + args.extension), verbose)
            del anthony



        
        


# Calling Main
main()
