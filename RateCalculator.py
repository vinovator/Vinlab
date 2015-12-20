# RateCalculator.py
# Python 2.7.6


"""
A python program that makes use of decorator. Our imaginary software 
consultant/ contractor uses this program to generate invoice for his 
various services
"""


class RateCatalog:
	"""
	These are distinct services provided by our software consultant
	1) Software contracts - billed per hour
	2) Software Training - billed by no. of participants per hour
	3) Speaking assignments - Fixed charge per speech session
	Other common requirements: 
	- Occasionally discouts are given if our consultant likes the client
	- VAT applicable for all rates
	Since these additional requirements are applicable for all services, 
	using decorator is a better option, rather than implementing the same
	logic in all methods. Also discounts or VAT can be selectively 
	applied for each service offered
	"""

	
	def __init__(self, discount=0, vat=0):
		"""
		Parameters Initialization
		keyword arguments:
		- If no explicit discount is passed, no discount assumed
		- If no explicit vat is passed, no vat markup assumed
		"""
		self.unit_hourly_rate = 100
		self.unit_training_rate = 250
		self.unit_speach_rate = 2000
		# Unless you convert to float, all fractions will be taken as 0
		self.discount = float(discount)/100
		self.vat = float(vat)/100
		
	
	def apply_discount(my_function):
		"""
		Decorator method that applies discount to a function
		"""
		def discountify(self, *args, **kwargs):
			"""
			Add discount to the rate
			Formula used >> rate * (1 - (discount/100))
			"""
			return (my_function(self, *args, **kwargs) * (1 - self.discount))
			
		return discountify # returns a function as output
		
	
	def apply_vat(my_function):
		"""
		Decorator method that applies VAT to a function
		"""
		def vatify(self, *args, **kwargs):
			"""
			Add discount to the rate
			Formula used >> rate * (1 + (discount/100))
			"""
			return (my_function(self, *args, **kwargs) * (1 + self.vat))
			
		return vatify # returns a function as output
		
	
	@apply_vat
	@apply_discount
	def get_contract_rate(self, numHours):
		"""
		Calculate total rate for contract assignments, charged per hour
		Input - total no of contract hours
		Output - total rate
		"""
		return self.unit_hourly_rate * numHours
	
	
	@apply_vat
	@apply_discount
	def get_training_rate(self, numHours, numAttendees):
		"""
		Calculate total rate for training, charged per hour per attendee
		Input - total no of hours and number of participants
		Output - total rate
		"""
		return self.unit_training_rate * numHours * numAttendees
		
	
	@apply_vat
	@apply_discount
	def get_speaking_rate(self, numSessions):
		"""
		Calculate rate for speaking assignments, charged per session
		Input - total no of sessions
		Output - total rate
		"""
		return self.unit_speach_rate * numSessions

		
if __name__ == "__main__":
		
	# Our guy gets a new job
	job = RateCatalog(discount=10, vat=14)
	
	# Contract is for 1 month, so 20 working days
	total_contract_rate = job.get_contract_rate(20*8)
	
	# And at end of contract give half-day traning to 10 people for 2 days
	total_training_rate = job.get_training_rate(2*4, 10)
	
	# Once training is over, give a speach to 200 people
	total_speaking_rate = job.get_speaking_rate(1)
	
	# So what is the total rate that client owes our guy
	total_rate = total_contract_rate + total_training_rate + total_speaking_rate
	
	# Lets print our invoice	
	print("Total Contract charge: ${}".format(total_contract_rate))	
	print("Total training charge: ${}".format(total_training_rate))	
	print("Total speaking charge: ${}".format(total_speaking_rate))
	print("*" * 30)
	print("Total invoice charge: ${}".format(total_rate))
	print("*" * 30)