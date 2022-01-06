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
        # Which axis was moved along while gathering data
        self.axis = axis
        # Rangeis used when removing outliers later on
        self.range = range

    # Removes outliers in the data. This is a first step and is only to remove
    # data which will interfere with the analysis. Later on there will be a
    # stricter cutoff. The default is 5 standard deviations.
    def DelOutliers(self, s_margin, verbose):
        for j in range(len(self.dataset) - 1):
            sigma = s_margin * self.dataset[j]["DAT"].std()
            upper = self.dataset[j]["DAT"].mean() + sigma
            lower = self.dataset[j]["DAT"].mean() - sigma
            self.dataset[j] = self.dataset[j][
                (self.dataset[j]["DAT"] > lower) & (self.dataset[j]["DAT"] < upper)
            ]

            if verbose:
                print(
                    self.dataset[j][
                        (self.dataset[j]["DAT"] < lower)
                        | (self.dataset[j]["DAT"] > upper)
                    ]
                )
            # print(self.dataset[j])

    def writeout(self, outpath, verbose):
        fileio.FileOut(outpath, self.dataset, verbose)

    # Function to take in values from linear regression and a data point then
    # subtracts the value of the trendine at x from dat, returning a float.
    def __ZML__(self, m, x, b, dat):
        # m, x, and b are standard representations of y=mx+b, but here it is dat=mx+b
        # normalises to linear regression. might become more complex in the future
        dat = dat - (m * x + b)
        return round(float(dat), 3)

    # This goes and normalizes to the zero mean line
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
            zml_data[k]["ZML"] = self.dataset[k].apply(
                lambda func: self.__ZML__(m, func[self.axis], b, func["DAT"]), axis=1
            )
            zml_data[k].drop(["DAT"], axis=1)
            zml_data[k] = zml_data[k][["X", "Y", "ZML", "ROW"]]
        self.dataset = zml_data
