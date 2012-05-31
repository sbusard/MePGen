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
	
	# TODO How to define an enum type?
	
	def __init__(self, type, left = None, right = None, range = None):
		self.type = type
		self.left = left
		self.right = right
		self.range = range
		
	def __str__(self):
		# TODO