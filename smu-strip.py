#!/usr/bin/python
#Strip extraneous data from an SMU data file
#Writes a file with same name prepended by 's-'
import sys
import time
import os
import pandas

tempfiles = []


for filename in sys.argv[1:]:
    #First, strip extraneous whitespace that can confuse pandas and store in temp file
    tempfilename = 's_temp-' + filename
    fout = open(tempfilename, "w")
    with open(filename, 'r') as fin:
       for line in fin:
          s = "".join(line.split())		#split on whitespace, rejoin the pieces, now no whitespace
          if len(s):      			#want to drop empty lines
             fout.write(s + '\n')                 #send to temp file
    fout.close()

    #Then, import temp file and re-export only useful columns
    outfilename = 's-' + filename
    inframe = pandas.read_csv(tempfilename)      #import csv file into a Pandas dataframe
    outframe = pandas.DataFrame({'TIME':inframe.TIME1,
                                 'VOLT':inframe.VOLT1,
                                 'CURR':inframe.CURR1 })  #create new frame from input
    outframe.to_csv(outfilename, index=False)

    #Finally, delete the temp file
    os.remove(tempfilename)





    
