# python 2.7.6
# myDecorator.py

"""
A simple decorator example in python
"""

class SimpleClass:
	"""
	A simple class with add and subtract methods, undecorated
	"""
	def __init__(self, num1, num2):
		"""
		Arguments initialization
		"""
		self.num1 = num1
		self.num2 = num2
		
	def add(self):
		return self.num1 + self.num2
		
	def sub(self):
		return self.num1 - self.num2
		
		
class DecoratedClass:
	"""
	A simple class with add and subtract methods, decorated
	"""	
	
	def __init__(self, num1, num2):
		"""
		Arguments initialization
		"""
		self.num1 = num1
		self.num2 = num2		
		
	def floatify(func):
		"""
		A decorator takes a function as input and returns a function as output
		"""
		def decorated_func(*args, **kwargs):
			return float(func(*args, **kwargs))
		return decorated_func
		
	@floatify
	def add(self):
		return self.num1 + self.num2
	
	@floatify
	def sub(self):
		return self.num1 - self.num2
	
	
if __name__ == "__main__":

	cls = SimpleClass(2,1)
	print(cls.add(), cls.sub())
	
	dcls = DecoratedClass(2,1)	
	print(dcls.add(), dcls.sub())