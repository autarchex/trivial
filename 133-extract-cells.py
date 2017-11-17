#!/usr/bin/python
#C. Roop  |  17 Nov 2017
#Script for processing data files of notebook pg 133, long term storage tests.
#I have 10 csv files each containing 8 cell measurements taken at same time.
#I want 8 csv files each containing a time-ordered series of measurements of
#one cell.  Cells are indexed 1..8.  Test times are ordered 1..10.
#Input filename convention is s-133-t-combined.csv, where 't' is the test number.
#All tests use the same TIME series.
#The first testpoint did not include cells 7 and 8.

import os
import pandas
import decimal as d


pwd = os.getcwd()               #present working directory
nInputs = 10        #number of input files
nOutputs = 8        #number of output files

infilenames = ["s-133-" + str(n+1) + "-combined.csv" for n in range(nInputs)]
outfilenames = ["cell-" + str(n+1) + "-data.csv" for n in range(nOutputs)]
print("Processing input files:")
[print("\t " + f) for f in infilenames]

#there are up to 17 columns (time, 8 volts, 8 currents) in the input file
#all columns need to be interpreted as Decimal values
colconvs = { n : d.Decimal for n in range(nOutputs * 2 + 1) }

#Pull input data into list of dataframes, each is a testpoint in range 1..10
inputframes = [ pandas.read_csv(f, converters=colconvs) for f in infilenames ]

#List of output dataframes, one per cell, containing TIME and CURR1..CURR8
outputframes = [ pandas.DataFrame() for n in range(nOutputs) ]

#All tests have identical TIME series, so grab one and distribute it
for odf in outputframes:
    odf['TIME'] = inputframes[0]['TIME']

#Copy, re-order, and re-name input columns to output columns
for t in range(nInputs):           #iterate on testpoints
    for c in range(nOutputs):      #iterate on cells
        idf = inputframes[t]
        odf = outputframes[c]
        column = 'VOLT' + str(c+1)
        if column in idf.columns:      #not all cells were present in early tests
            odf['VOLT' + str(t+1)] = idf[column]  #copy and rename by test number
            column = 'CURR' + str(c+1)
            odf['CURR' + str(t+1)] = idf[column]  #repeat for current column
        else:
            pass   #TODO: put a placeholder into file for missing tests.
                   #Might not be necessary

print("Saving re-ordered data to output files:")
for n in range(nOutputs):
    outputframes[n].to_csv(outfilenames[n], index=False)
    print("\t " + outfilenames[n])
