#!/usr/bin/python
#Strip whitespace and empty lines from a file
#Writes a file with same name prepended by 's-'
import sys

for filename in sys.argv[1:]:
    ofilename = 's-' + filename
    fout = open(ofilename, "w")
    with open(filename, 'r') as fin:
       for line in fin:
          s = "".join(line.split())		#split on whitespace, rejoin the pieces, now no whitespace
          if len(s):      #want to drop empty lines
             fout.write(s + '\n')                 #send to output file

    
