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
		

class Concat(Regex):
	
	def __init__(self, left, right):
		self.left = left
		self.right = right
		
	def __str__(self):
		return "(" + str(self.left) + " . " + str(self.right) + ")"
		
	def copy(self):
		return Concat(self.left.copy(), self.right.copy())
		

class Choice(Regex):

	def __init__(self, left, right):
		self.left = left
		self.right = right
		
	def __str__(self):
		return "(" + str(self.left) + " | " + str(self.right) + ")"
		
	def copy(self):
		return Concat(self.left.copy(), self.right.copy())
		
		
class Repeat(Regex):
	
	def __init__(self, child):
		self.child = child
	
	def __str__(self):
		return "(" + str(self.child) + ")*"
		
	def copy(self):
		return Concat(self.child.copy())


class Range(Regex):
	
	def __init__(self, regrange):
		self.range = regrange
		
	def __str__(self):
		return "[" + str(self.range) + "]"
		
	def copy(self):
		return Range(self.range)
		
		
class Custom(Regex):
	"""
	Custom regex is a regex defined by an automaton.
	"""
	
	def __init__(self, automaton):
		self.automaton = automaton
		
	def __str__(self):
		return "Custom(" + str(self.automaton) + ")"
	
	def copy(self):
		return Custom(self.automaton.copy())