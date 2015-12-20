# getHttpHeader.py
# Python 2.7.6

import requests
from requests.auth import HTTPDigestAuth
import getpass # To mask the password typed in

# Replace with the correct URL
url = "http://some_url"

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
# The default prompt, if none is specified is “Password:”
myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), getpass.getpass()), verify=True)
#print (myResponse.status_code)

myRequestHeader = myResponse.request.headers
myResponseHeader = myResponse.headers

print ("Request headers: ") # Gets the header sent in Request
for key in myRequestHeader:
	print (key, myRequestHeader[key])

print ("Response headers: ") # Gets the header from Response 
for key in myResponseHeader:
	print (key, myResponseHeader[key])

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
	print ("ok")
	
else:
  # If response code is not ok (200), print the resulting http error code with description
	myResponse.raise_for_status()