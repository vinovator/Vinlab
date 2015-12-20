# Logger.py
# Python2.7.6
# For more details - https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
# logging.error - just displays the error message
# logging.exception - displays the stack trace along with the error message

import logging # For logs
import sys # To read parameters from command line

# Define the format of the logging
logging.basicConfig(filename='Logger.log', 
					format="%(asctime)s: %(levelname)s: %(message)s",
					datefmt='%m-%d-%Y %I:%M:%S %p',
					filemode="w", 
					level=logging.DEBUG)


def calc(num1, num2, operator):
	
	if (operator == "+"):
		try:
			result = num1 + num2
			logging.info("Value returned is {0}".format(result))
			return result
		except Exception as e:
			print("Error occured", e)
			logging.error(e)
		
	elif (operator == "-"):
		try:
			result = num1 - num2
			logging.info("Value returned is {0}".format(result))
			return result
		except Exception as e:
			print("Error occured", e)
			logging.error(e)
		
	elif (operator == "*"):
		try:
			result = num1 * num2
			logging.info("Value returned is {0}".format(result))
			return result
		except Exception as e:
			print("Error occured", e)
			logging.error(e)
		
	elif (operator == "/"):
		try:
			result = num1 / num2
			logging.info("Value returned is {0}".format(result))
			return result
		except Exception as e:
			print("Error occured", e)
			logging.error(e)
		
	else:
		print("Invalid operator: {0}".format(operator))
		logging.warning("Invalid operator : {0}".format(operator))
		return None
		
try:
	num1 = int(sys.argv[1])
	num2 = int(sys.argv[2])
	operator = str(sys.argv[3])
	logging.info("num1: {0}; num2: {1}; operator: {2}".format(num1, num2, operator))
	
	print calc(num1, num2, operator)
except Exception as e:
	print("Error occured: ", e)
	logging.error(e)