# python 2.7.6.
# portScanner.py

import socket
from datetime import datetime
import sys

# Here we are scanning your own terminal
# Replace this with gethostbyname("host") to scan a remote host 

# scanServer = "localhost"
scanServer = socket.gethostname()
scanServerIP = socket.gethostbyname(scanServer)

time_start = datetime.now()
print("Scanning IP {0} started at {1}".format(scanServerIP, time_start))

try:
	# Scanning from port range. Scan of each port might take a second
	for port in range (1, 200):
		# We opt for TCP connections using socket_stream, as against UDP connections using socket_dgram
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Using connect_ex does not raise exception for normal connection denial
		# Useful to skip the port and move on to next port
		result = sock.connect_ex((scanServerIP, port))
		if(result == 0):
			print("Port {0} is open".format(port))
		sock.close()
		
except KeyboardInterrupt:
	print("Stopping....")
	sys.exit()

except socket.error as e:
	print e
	sys.exit()

time_end = datetime.now()
print("Scanning completed at {0}".format(time_end))
print("Total time took for scanning: {0}".format(time_end - time_start))