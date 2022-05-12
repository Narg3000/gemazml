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

fileio.py - reads and writes files
Module for reading and writing files
"""
# Imports!
import pandas as pd
import csv


# Read in function, returns a list of dataframes.
# There is a way to do this with a single numpy array but I don't know it yet
# so here is this. Takes string argument
def FileIn(infile):
    if type(infile) != str:
        raise Exception("infile must be of type string")
    print(infile)
    data = pd.read_fwf(infile)  # Read in the data
    data.X = pd.to_numeric(data['X'], errors="coerce")  # Turn things into numvers
    data.Y = pd.to_numeric(data['Y'], errors="coerce")
    data.READING = pd.to_numeric(data['READING'], errors="coerce")
    data.LINE = pd.to_numeric(data['LINE'], errors="coerce")
    data = (
        data[["X", "Y", "READING", "LINE"]]
        .dropna()
        .rename(columns={"READING": "DAT", "LINE": "ROW"})
    )  # Clear out NaN values
    list_o_data = []

    for i in range(int(data["ROW"].max()) + 1):
        list_o_data.append(data[data.ROW == i])
    return list_o_data


# Function to write out the data to a new file. Non returning function
# Takes argument "outpath", location of file to write.
def FileOut(outpath, final_dat, verbose):
    # Some now redundant checks but better safe than sorry
    if type(outpath) != str:
        raise Exception(f"outpath must be of type string but is type {type(outpath)}")

    # creates the file and puts in the header
    with open(outpath, "w") as file:
        file.write("           X           Y     READING        LINE\n")
    if verbose:
        print(f"Header Written to {outpath}")


    for df in final_dat:  # itterates over the array
        df["ROW"] = df.astype(
            {"ROW": int}
        )  # Converts the row from float64 to int64, needed for file output
        """
        In order to get this working as a fixed width file I am using the inbuilt df.to_string method with
        formatting specified. Somthing to note with this is that regarless of the formatting specified pandas
        goes and adds a space after every collumn excpet the last so in order to get 12 wide columns you actually
        have to start counting from zero on all columns after the first, hence the 12, 11, 11, 11 notation. 
        """
        with open(outpath, "a") as file:
            file.write(df.to_string(col_space = 11, header = False, index = False, max_colwidth=13,
            formatters={
                'X': "{:>12.3f}".format,
                'Y': "{:>11.3f}".format,
                'READING': "{:>11.3f}".format,
                'LINE': "{:>11.d}".format}
                ) + '\n')

# Basically a copy of the above but it uses magical elves to write file headers. Or somthing 
def CatOut(outpath, final_dat, newfile, verbose):
    if type(outpath) != str:
        raise Exception(f"outpath must be of type string but is type {type(outpath)}")
    # If we are creating a new file we must write the header!
    if newfile: 
        with open(outpath, "w") as file:  # creates the file and puts in the header
            file.write("           X           Y     READING        LINE\n")
        if verbose:
            print("Header Written")

    for df in final_dat:  # itterates over the array
        df["ROW"] = df.astype({"ROW": int})  # Converts the row from float64 to int64, needed for file output
        # See comment in FileOut() for explenation. 
        with open(outpath, "a") as file:
            file.write(df.to_string(col_space = 11, header = False, index = False, max_colwidth=13,
            formatters={
                'X': "{:>12.3f}".format,
                'Y': "{:>11.3f}".format,
                'READING': "{:>11.3f}".format,
                'LINE': "{:>11.d}".format}
                ) + '\n')
