# RestfulPostClient.py
# Python 2.7.6

import requests
from requests.auth import HTTPDigestAuth
# import json # Json module is not required as we are directly passing json to requests


# Replace with the correct URL
url = "http://api_url"

# Replace with appropriate header
header = {"content-type": "application/json"}

# Replace with correct payload
payload = {"some_key": "some_data"}

myResponse = requests.post(url, 
			# data = json.dumps(payload), # takes a dict and connverts into json
			json = payload # directly pass a dict, it will be auto-converted to json
			headers = header, 
			auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")))

if(myResponse.ok):
	print (myResponse.status_code, myResponse.reason, " Your post operation was successful")
else:
  	# If response code is not ok (200), print the resulting http error code with description
	myResponse.raise_for_status()