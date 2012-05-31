class Regex():
	"""
	A Regex represents a regular expression. Each Regex has a type
	(CONCAT, CHOICE, REPEAT, RANGE).
	
	For example, the regular expression (a.(b|c))* is represented by
	(	REPEAT, 
		(	CONCAT,
			(RANGE('a')),
			(	CHOICE,
				(RANGE('b')),
				(RANGE('c'))
			)
		)
	)
	"""
	
	# Regex types
	CONCAT, CHOICE, REPEAT, RANGE = range(4)
	
	def __init__(self, regtype):
		self.type = regtype
		

class Concat(Regex):
	
	def __init__(self, left, right):
		super().__init__(Regex.CONCAT)
		self.left = left
		self.right = right
		
	def __str__(self):
		return "(" + str(self.left) + " . " + str(self.right) + ")"
		

class Choice(Regex):

	def __init__(self, left, right):
		super().__init__(Regex.CHOICE)
		self.left = left
		self.right = right
		
	def __str__(self):
		return "(" + str(self.left) + " | " + str(self.right) + ")"
		
		
class Repeat(Regex):
	
	def __init__(self, child):
		super().__init__(Regex.REPEAT)
		self.child = child
	
	def __str__(self):
		return "(" + str(self.child) + ")*"


class Range(Regex):
	
	def __init__(self, regrange):
		super().__init__(Regex.RANGE)
		self.range = regrange
		
	def __str__(self):
		return "[" + str(self.range) + "]"