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

grid-process-class.py - THE NORMALIZER (class)
Class definitions and methods used for data normalization.
"""
import numpy as np
import pandas as pd
import fileio
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# This is the big class where everything happens


class Normalizer:
    def __init__(self, infile, axis, range):
        self.dataset = fileio.FileIn(infile)
        self.infile = infile
        # Which axis was moved along while gathering data
        self.axis = axis
        # Rangeis used when removing outliers later on
        self.range = range

    # Removes outliers in the data. This is a first step and is only to remove
    # data which will interfere with the analysis. Later on there will be a
    # stricter cutoff. The default is 5 standard deviations.
    # NEW in v 0.0.2, now  just use the min and max vlaues of the earths B field
    def DelOutliers(self, verbose):
        for j in range(len(self.dataset) - 1):
            upper = 70000
            lower = 20000
            self.dataset[j] = self.dataset[j][
                (self.dataset[j]["DAT"] > lower) & (self.dataset[j]["DAT"] < upper)
            ]

    # Function to take in values from linear regression and a data point then
    # subtracts the value of the trendine at x from dat, returning a float.
    def __ZML__(self, m, x, b, dat):
        # m, x, and b are standard representations of y=mx+b, but here it is dat=mx+b
        # normalises to linear regression. might become more complex in the future
        dat = dat - (m * x + b)
        return round(float(dat), 3)

    # This goes and normalizes to the zero mean line

    # IMPORTANT NOTE: THIS DELETES THE DAT COLUMN AND REPLACES IT WITH ZML. THE CODE BELOW THIS MUST 
    # BE EITHER REWRITTEN OR ONLY BE RAN IN A CERTAIN ORDER. THE CHOICE IS YOURS!
    def ZmlInator(self):
        zml_data = []
        for k in range(len(self.dataset) - 1):
            # k is used to index, and because we need to modify we need to work on the arrays themselves
            lin_line = LinearRegression().fit(
                self.dataset[k][[self.axis]], self.dataset[k]["DAT"]
            )  # run regression on dataset
            zml_data.append(self.dataset[k].copy())
            m, b = lin_line.coef_, lin_line.intercept_  # Get coefficents and intercept
            # goes through array and runs the ZML function on every row, storing the results in the copy, zml data
            zml_data[k]["ZML"] = self.dataset[k].apply(lambda func: self.__ZML__(m, func[self.axis], b, func["DAT"]), axis=1)
            zml_data[k].drop(["DAT"], axis=1)
            zml_data[k] = (zml_data[k][["X", "Y", "ZML", "ROW"]])

        self.dataset = zml_data

    # Function to destagger the data, taking a small offset and shifting the axis values slightly.
    # This operates by adding to the odd columns and subtracting from the even. This avoids issues with the 
    # duplictae rows which are not stored next to oneanother. 
    def destaggerer(self, ammount, verbose):
        if type(ammount) != float: raise Exception("Input must be float!")
        if verbose: print(f"destaggering data from file {self.infile} by +/- {ammount}")

        for i in range(len(self.dataset) - 1):
            if (self.dataset[i].iloc[0]['ROW'] % 2):
                self.dataset[i][self.axis] = self.dataset[i][self.axis] + ammount
            else:
                self.dataset[i][self.axis] = self.dataset[i][self.axis] - ammount
    
    # Function to cut out slightly anamolous data. Less useful with the well designed DelOutliers method
    # but still can be helpful
    def limitRange(self):
        normalized = []
        for k in range(len(self.dataset)):
            up = (
                self.dataset[k].ZML.mean() + self.range
            )  # Takes mean of row and sets bound based around it
            low = self.dataset[k].ZML.mean() - self.range  # (±range)
            # moves data that falls within bounds to new array. New name used to allow for retention
            # of diffrent processes throughout. Might be changed in next revision
            normalized.append(
                self.dataset[k][
                    (self.dataset[k].ZML < up) & (self.dataset[k].ZML > low)
                ]
            )
        # Is this inefficent? Yes. Does it work? Also yes. Will be fixed up later on
        self.dataset = normalized
    def writeout(self, outpath, verbose):
        fileio.FileOut(outpath, self.dataset, verbose)

    def concatOut(self, outpath, verbose, is_append):
        fileio.CatOut(outpath, self.dataset, is_append, verbose)