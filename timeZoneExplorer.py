# Python 2.7.6
# timeZoneExplorer.py

from pytz import timezone, common_timezones # import all_timezones for more exhaustive list
from datetime import datetime
import os

# Log file will be created in the same folder as the python script
my_path = "."
log_path = os.path.join(my_path + "/" + "loc_log.txt")

fmt = "%Y-%m-%d %H-%M-%S %Z%z"

fixed_length = 32

with open(log_path, "w") as my_log:
	for zone in common_timezones:
		local_time = datetime.now(timezone(zone)).strftime(fmt)
		space = fixed_length - len(zone)
		
		#my_log.write("{0} : {1}".format(zone, local_time))
		my_log.write("{0}{1}:{2}".format(zone, " "*space, local_time))
		#my_log.write(zone + " "* space + ":" + local_time)
		my_log.write("\n")
	
print ("Done")