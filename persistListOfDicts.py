# persistListOfDicts.py
# Python 2.7.6


import json
import os
import pickle # To persist each dict

json_path = "./JSON"
	
# Write dicts into a pickle file each
for num in range(1, 100):	
	my_dict = dict()
	my_dict["loop"] = num
	my_dict["name"] = "name - " + str(num)
	
	file_name = "{0}.p".format(num)
	
	with open(os.path.join(json_path + "/" + file_name), mode="wb") as pickl:
		pickle.dump(my_dict, pickl)
	
print("Done. Write complete")

my_lst = list()
	
# Read the pickle files into a list
for num in range (1, 100):
	file_name = "{0}.p".format(num)
	
	with open(os.path.join(json_path + "/" + file_name), mode="rb") as pickl:
		my_lst.append(pickle.load(pickl))

print ("Done. Read complete")
		
for item in my_lst:
	print(item)