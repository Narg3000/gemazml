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
import regex as re


# Read in function, returns a list of dataframes.
# There is a way to do this with a single numpy array but I don't know it yet
# so here is this. Takes string argument
def FileIn(infile):
    if type(infile) != str:
        raise Exception("infile must be of type string")
    with open(infile, "r") as file:
        data = file.read()  # Reads data in as string
    #  print(data)
    data = re.sub("[^\S\n\r]+", ",", data)  # Some regular expression to turn it into
    data = re.sub("\n,", "\n", data)  # standard csv formatted string
    csv_working = data.split("\n")
    # Now we need to turn the data into a list because reasons (specifically
    # because the csv librairy needs lists to work right)
    csv_processed = csv.reader(csv_working)
    # Header can be discarded
    header = next(csv_processed)
    del header  # Do some garbage collection, always helpful!
    # print(csv_working)     Makes sure everything worked
    list_o_data = []  # this will become the list of dataframes
    temp_arr = [
        next(csv_processed)
    ]  # empty list used for slicing up the data. Inital value of first row
    prev = temp_arr[0][3]  # inital value for row number
    for line in csv_processed:  # Itterates over the csv file
        if line == []:
            pass  # For some reason the csv terminates with nul list, I
        #           just check if it exists and ignore
        # line[3] is index where row is stored, we organise data by row.
        # if prev!= line[3], the rows are diffrent so we save the temp_arr as a dataframe to the final output
        elif prev != line[3]:
            list_o_data.append(
                pd.DataFrame(temp_arr, columns=["X", "Y", "DAT", "ROW"], dtype=float)
            )  # stores as dataframe
            temp_arr = [
                line  # By redefinign the array it clears all stored values
            ]  # and starts over. stores new row
            prev = line[3]  # redefine prev
        else:  # if not new row, just adds data to current row
            temp_arr.append(line)

    return list_o_data


# Function to write out the data to a new file. Non returning function
# Takes argument "outpath", location of file to write.
def FileOut(outpath, final_dat, verbose):
    if type(outpath) != str:
        raise Exception(f"outpath must be of type string but is type {type(outpath)}")
    with open(outpath, "w") as file:  # creates the file and puts in the header
        file.write("X Y READING LINE \n")
    if verbose:
        print("Header Written")

    for df in final_dat:  # itterates over the array
        df["ROW"] = df.astype(
            {"ROW": int}
        )  # Converts the row from float64 to int64, needed for file output
        """
        Using pandas standard csv method to write out the data. Headers and indexes are turned off
        and the seperator character has been turned into a tab instead of comma. Somthing to note
        is that I open the file in append mode so that the dataframes are consecutively written to the
        bottom of the csv.
        """

        df.to_csv(outpath, sep="\t", header=False, index=False, mode="a")
        if verbose:
            print("printed a line!")
