#!/apps/admin/tools.x86_64/python/2.7.3/bin/python
# Takes a path to a file, opens the file, parses the data into chunks, looks for duplicates, and prints those to a file.
#
#
#
import os
import sys
import sets
import argparse
from glob import glob

ap = argparse.ArgumentParser()
ap.add_argument("--files","-f",dest="files",nargs='+',action="store",required=False,help="Use the accounting records in these files",
    default = glob('/var/spool/torque/server_priv/accounting/*'))
ap.add_argument("--output","-o",dest="output",nargs='+',action="store",required=False,help="Output file location",
    default = glob('/tmp/duplicate_job_ids.txt'))

args=ap.parse_args()

#Parse input files. Borrowed from Derek's qhistory script
def parse_files(filenames, debug):
    texts=[]
    for fname in filenames:
        f = open(fname,'r')
        texts.append(f.read())
        f.close
    return texts

#Function to clear output files and ensure they can be written to
def clear_output(filenames, debug):
    for fname in filenames:
       clearfile = open(fname,'w')
       clearfile.write(" ")
       clearfile.close()
    return clearfile

#Declare variables and set static information
list_of_files = set()
pre_split_line=" "
list_of_logs=" "

try:
    path_to_file=str(args.files)
except:
    print "Invalid path for accounting data."
    print args.files
    exit(0)

#capture the output of parse_files() and then capture the output of the split strings.
text_of_file="".join(parse_files(args.files, 0))
split_file_text=text_of_file.split(" ")

#Step through each line that was split previously and find the string ";S;". If found, store the line of text split on the ; delimiter. Merge into a single string with new lines.
for line in split_file_text:
    if (line.find(";S;") != -1 ):
       line_text=line.split(";")
       pre_split_line+="\n" + str(line_text[2])

#Split the text into a list using the splitlines() string function.
textlist=pre_split_line.splitlines()

#Clear file and make sure it can be written to
try:
    file_location=clear_output(args.output, 0)
except:
    print "No output file given"
    exit(0)

try:
    output=open(str(args.output),'a')
except:
    print "Could not open " + str(args.output) + " for appending"
#Step through the list and count repeat occurances. If the number of occurances is > 1 write the line to a file.
for line in textlist:
    count = textlist.count(line)
    if (count > 1):
	output.write(line + " \n")
print args.output
output.close()
