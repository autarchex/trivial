#!/usr/bin/python
#Combine SMU output files (csv) having identical time series into one file.
#Extracts VOLT and CURR from each input file, and writes them as VOLTn and CURRn
#in the output file.
#Extracts TIME from first input file, and writes it to TIME in output file.
#No other input columns make it to the output.
#Output columns are ordered as: TIME, VOLT1, ... VOLTn, CURR1, ... CURRn
#This will make it easier to read them back in for arbitrary sample sizes
#Input file name convention is xxx-e-n.csv, where xxx-e will be combined together
#and n is the sample number.
#Output file name convention is xxx-e-combined.csv .
#If given argument of xxx-e on command line, combine all files in working directory
#that match that file name pattern; if -if switch is given, it is followed by
#specific filenames to combine instead.
import sys
import os
import pandas
import decimal as d

infilepattern = sys.argv[1]
outfilename = infilepattern + "-combined.csv"
fout = open(outfilename, "w")

pwd = os.getcwd()
csvfiles = []
for f in os.listdir(pwd):
    if f.endswith(".csv"):
        csvfiles.append(f)      #generate list of all .csv files in directory
infiles = []
for f in sorted(csvfiles):
    if f.startswith(infilepattern):
        if not f.endswith("-combined.csv"):      #skip previous outputs
            infiles.append(f)       #now we have list of all our input files
print("Input files: " + str(infiles))

#import all files as dataframes, store in a list
frames = [pandas.read_csv(f, converters={'TIME':d.Decimal, 'VOLT':d.Decimal, 'CURR':d.Decimal}) for f in infiles]

#TODO: create new dataframe, 'outframe'
outframe = pandas.DataFrame()
outframe['TIME'] = frames[0].TIME      #add time data to output


#move voltage data to output
for n in range(len(frames)):
    colname = "VOLT" + str(n + 1)
    incol = frames[n].VOLT
    outframe[colname] = incol

#move current data to output
for n in range(len(frames)):
    colname = "CURR" + str(n + 1)
    incol = frames[n].CURR
    outframe[colname] = incol

print("Output file: " + outfilename)
outframe.to_csv(outfilename, index=False)
