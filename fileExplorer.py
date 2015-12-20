# fileExplorer.py
# python 2.7.6

import os
# defaultdict is used to have keys created if it doesn't exist or appended it if exists
from collections import defaultdict

folder_count = 0
file_count = 0
loop_count = 0
file_extn = defaultdict(int)

my_path = "C://folder_name"
log_path = os.path.join(my_path + "/" + "file_log.txt")

with open(log_path, "w") as my_log:
	for path, folders, files in os.walk(my_path):
		loop_count += 1
		my_log.write("\n")
		
		my_log.write(str(path))
		my_log.write("\n")
		
		my_log.write(str(folders))
		folder_count += len(folders)
		
		my_log.write("\n")
		
		my_log.write(str(files))
		file_count += len(files)
		# Get the count of files by file extension
		for file in files:
			extn = os.path.splitext(file)[1]
			file_extn[extn] += 1
		
		my_log.write("\n")
		my_log.write("*****************")
		my_log.write("\n")
		my_log.write("\n")

print("Scanning complete")
#print("There are {0} loops".format(loop_count))
print("There are {0} folders".format(folder_count))
print("There are {0} files".format(file_count))
print ("Count per file type:")
for extn in file_extn:
	print (extn, file_extn[extn])