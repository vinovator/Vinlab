# jsonToCSV.py
# Python 2.7.6

'''
Place all the json payloads as separate text files in base folder
Program will extract each payload and generate single csv file
csv file will have key value pairs in separate columns
'''

import json
import csv
import os

# Folder path where files are placed
base_path = "./Json_To_Csv"

# Name of the output csv file
output_csv_file_name = "output_csv.csv"


def loopDict(in_dict, csv_writer, append_string):

	for key in sorted(in_dict):
	
		# Some values can be list of dictionaries
		if(isinstance(in_dict[key], list)):
			for item in in_dict[key]:
			
				# Extract each item from list and check if it is dict
				if isinstance(item, dict):
					loopDict(item, csv_writer, append_string + key + ":")
					
				# If the item in list is not a dict, then write it directly
				else:
					csv_writer.writerow([append_string + key, in_dict[key]])
		
		# If the value is a dict, loop again		
		elif(isinstance(in_dict[key], dict)):
			loopDict(in_dict[key], csv_writer, append_string + key + ":")
			
		else:
			csv_writer.writerow([append_string + key, in_dict[key]])
	

def main():

	# Counts the number of payloads processed
	loop_success_count = 0
	
	loop_failure_count = 0
	
	loop_skip_count = 0
	
	# Save all JSON payloads as text files within folder
	for path, folders, files in os.walk(base_path):
		for file in files:
			# Scan all text files to extract JSON payload
			if (os.path.splitext(file)[1] in (".txt")):
				#Increment the counter
				loop_success_count += 1
				
				print ("Scanning file - {0}".format(file))
				
				with open(os.path.join(base_path + "/" + file) , "r") as txt_file:
					json_txt = ""
					for each_line in txt_file:
						json_txt += each_line
				#print json_txt
			
				# Load the json string into a dict variable
				try:
					data_dict = json.loads(json_txt)
					print("JSON successfully extracted from {0}".format(file))
				except Exception as e:
					print ("{0} : {1}\n".format(file, e))
					loop_success_count -= 1 # Files that cannot be processed should be excluded from count
					loop_failure_count += 1
					continue # Move on to next loop
			
				with open(os.path.join(base_path + "/" + output_csv_file_name), "ab") as csv_file:
					#csv_writer = csv.DictWriter(csv_file, fieldnames = ["key", "Value"])
					#csv_writer.writeheader()
					csv_writer = csv.writer(csv_file)
					
					# Emply row is passed as a separator between payloads
					if (loop_success_count > 1):
						csv_writer.writerow(["", ""])
						
					# Write the file name (without extn) as title 
					csv_writer.writerow([loop_success_count, os.path.splitext(file)[0]])
					
					# Header row
					csv_writer.writerow(["Key", "Value"])
					
					# Loop through each value, check if it is string or list or dict and extract values	
					loopDict(data_dict, csv_writer, "")
						
					print ("Scanning complete\n")
					
			else:
				# Files which are not text files are skipped
				loop_skip_count += 1
				print ("Scanning skipped for - {0}\n".format(file))
	
	# All files scanned
	print("Done - {0} files processed Successfully; {1} files failed; {2} files skipped\n".format(loop_success_count, loop_failure_count, loop_skip_count))


if __name__ == "__main__":
    main()		
	
