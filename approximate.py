# salberico 2017

EPSILON = 0.00000001

def print_add(initial):
	"""
	Print cascade of addition for 
	first, second, third, ... differences
	"""
	l = len(initial)
	
	for i in range(l-1):
		print(initial)
		
		for sub in range(l-i-1,0,-1):
			initial[sub] = initial[sub] - initial[sub-1]
		del initial[0]
		print(initial)
		
	return initial

def get_delta(initial):
	"""
	Get cascade of subtraction for 
	first, second, third, ... differences
	"""
	l = len(initial)
	new = []
	
	for i in range(l-1):
		for sub in range(l-i-1,0,-1):
		
			initial[sub] = initial[sub] - initial[sub-1]
			
		del initial[0]
		new.append(initial[0])
		
	return new

def mult(a, d):
	""" returns factorial(a+d)/factorial(a), assumes d >= 0 """
	prod = 1
	
	for i in range(a, a+d):
		prod *= i
		
	return prod

def str_long(d):
	""" 
	returns a string representing a large int 'd'
	for printing purposes 
	"""
	if abs(d) < 10**5:
		return str(d)
		
	int_str = str(abs(d))
	exponent = len(int_str) - 1

	return ("-" if d < 0 else "") + int_str[0] + '.' + int_str[1:6] + 'e+' + str(exponent)


class Polynomial():
	""" 
	Represents n'th degree polynomial
	Initialize with coefficient list, or string of polynomial type.
	"""

	def __init__(self, cof=[], cut=1):
		""" 
		Initializes with string or list
		'cut' will get rid off all trailing zeroes
		"""
	
		if type(cof) == str:
			self.coefficients = Polynomial.from_string(cof).coefficients
			return
			
		if cut:
			fnon_zero = 0
			for i in range(len(cof)-1,-1,-1):
				if abs(cof[i]) > EPSILON:
					fnon_zero = i + 1
					break
			self.coefficients = cof[:fnon_zero]
		else:
			self.coefficients = cof

	def from_string(s):
		""" 
		returns a polynomial from given string 's'
		attempts to read string given human format, for example
		2.4x^3 + 5x - x + 1, but it should be pretty robust
		"""

		s = s.strip().strip('+') + " "
		num = 0 # default number, which will never be a cof
		result = []
		_space = 0

		fdigit = -1 # first digit in token of cofs
		fpow = -1 # first digit in token of powers
		_carr = 0 # if previous character is ^

		floating = 0
		max_pow = 0

		invert = 0
		coefficients = []

		for i, c in enumerate(s):

			if c == '.':
				floating = 1


			if (c.isalpha() and fdigit == -1):
				num = -1 if invert else 1
				invert = 0
				if s[i+1] != '^':
					result.append((num,1))
					max_pow = 1 if not max_pow else max_pow

			if (c.isdigit() or c == '.') and not _carr and fpow == -1:
				if fdigit == -1:
					fdigit = i;
			elif fdigit != - 1:
				if floating:
					n = float(s[fdigit:i])
				else:
					n = int(s[fdigit:i])

				num = -n if invert else n

				if c.isalpha() and s[i+1] != '^':
					result.append((num,1))
					max_pow = 1 if not max_pow else max_pow
				elif not c.isalpha():
					result.append((num,0))

				invert = 0
				fdigit = -1
				floating = 0

			if _carr:
				fpow = i
			if fpow != -1 and not c.isdigit():
				p = int(s[fpow:i])
				result.append((num,p))
				if p > max_pow:
					max_pow = p
				fpow = -1

			_carr = 1 if c == '^' else 0
			invert = not invert if c == '-' else invert

		coefficients = [0] * (max_pow+1)
		for pair in result:
			coefficients[pair[1]] += pair[0]

		return Polynomial(coefficients)

	def process_var(self, x):
		""" 
		process incoming argument 'x' 
		returning the correct polynomial representation 
		"""
		if (type(x) != Polynomial):
			if (type(x) == list):
				x = Polynomial(x)
			elif (type(x) == int):
				x = Polynomial([x])
			elif (type(x) == str):
				x = Polynomial.from_string(x)
		return x

	def trim(self):
		""" cuts trailing zeroes """
		i = self.degree
		while(not self.coefficients[i] and i >= 0):
			i -= 1
		self.coefficients = self.coefficients[:i+1]

	def sign(self, i):
		""" returns sign of coefficient at i """
		return "-" if self.coefficients[i] < 0 else "+"

	def __add__(self, x):
		""" 
		Adds 'x' to first polynomial, p+x
		"""
		new_sum = Polynomial()
		x = self.process_var(x)

		if (x.degree < self.degree):
			new_sum.coefficients = self.coefficients[:]
			for i in range(x.degree+1):
				new_sum.coefficients[i] = x.coefficients[i] + self.coefficients[i]
				if (new_sum.coefficients[i] < EPSILON):
					new_sum.coefficients[i] = 0
		else:
			new_sum.coefficients = x.coefficients[:]
			for i in range(self.degree+1):
				new_sum.coefficients[i] = x.coefficients[i] + self.coefficients[i]
				if (new_sum.coefficients[i] < EPSILON):
					new_sum.coefficients[i] = 0
		new_sum.trim()
		return new_sum

	def __sub__(self, x):
		""" 
		Subtracts 'x' to first polynomial, p+x
		"""
		new_sum = Polynomial()
		x = self.process_var(x)

		if (x.degree < self.degree):
			new_sum.coefficients = self.coefficients[:]
			for i in range(x.degree+1):
				new_sum.coefficients[i] = x.coefficients[i] - self.coefficients[i]
				if (new_sum.coefficients[i] < EPSILON):
					new_sum.coefficients[i] = 0
		else:
			new_sum.coefficients = x.coefficients[:]
			for i in range(self.degree+1):
				new_sum.coefficients[i] = x.coefficients[i] - self.coefficients[i]
				if (new_sum.coefficients[i] < EPSILON):
					new_sum.coefficients[i] = 0
		new_sum.trim()
		return new_sum

	def __mul__(self, x):
		""" 
		Multiplies 'x' by first polynomial, p*x
		"""
		x = self.process_var(x)

		new_prod = Polynomial([0] * (self.degree + x.degree+1), 0)

		for a in range(self.degree+1):
			for b in range(x.degree+1):
				new_prod.coefficients[a+b] += self.coefficients[a] * x.coefficients[b]
		return new_prod

	# assign reverse multiplication
	__rmul__ = __mul__

	def __pow__(self, x):
		""" 
		Exponentiates polynomial by x, p^x p**x
		"""
		new_pow = Polynomial([1])

		for i in range(x):
			new_pow *= self.coefficients
		return new_pow

	def __str__(self):
		""" 
		Converts polynomial to a nice formated string for printing
		"""
		new_str = ""
		for i in range(self.degree,-1,-1):
			if abs(self.coefficients[i]) < EPSILON:
				# co of 0
				continue
			elif (abs(self.coefficients[i])-1) < EPSILON:
				# co of 1
				if (i == 1):
					# degree of 1
					if (i == self.degree):
						# first term
						new_str += '-' if self.coefficients[i] < 0 else '' + "x"
					else:
						new_str += " %s x" % self.sign(i)
				elif (i == 0):
					# degree of 0
					if (i == self.degree):
						# first term
						new_str += "%g" % self.coefficients[i]
					else:
						new_str += " %s %g" % (self.sign(i), abs(self.coefficients[i]))
				else:
					# if degree > 1
					if (i == self.degree):
						# first term
						new_str += "%sx^%d" % ("-" if self.coefficients[i] < 0 else "", i)
					else:
						new_str += " %s x^%d" % (self.sign(i), i)
			else:
				# co > 1
				if (i == 1):
					# degree of 1
					if (i == self.degree):
						# first term
						try:
							new_str += "%gx" % self.coefficients[i]
						except OverflowError:
							new_str += str_long(self.coefficients[i]) + "x"
					else:
						try:
							new_str += " %s %gx" % (self.sign(i), abs(self.coefficients[i]))
						except OverflowError:
							new_str += " %s %sx" % (self.sign(i), str_long(abs(self.coefficients[i])))
				elif (i == 0):
					# degree of 0
					if (i == self.degree):
						# first term
						try:
							new_str += "%g" % self.coefficients[i]
						except OverflowError:
							new_str += str_long(self.coefficients[i])
					else:
						try:
							new_str += " %s %g" % (self.sign(i), abs(self.coefficients[i]))
						except OverflowError:
							new_str += " %s %s" % (self.sign(i), str_long(abs(self.coefficients[i])))
				else:
					# if degree > 1
					if (i == self.degree):
						# first term
						try:
							new_str += "%gx^%d" % (self.coefficients[i], i)
						except OverflowError:
							new_str += "%sx^%d" % (str_long(self.coefficients[i]), i)
					else:
						try:
							new_str += " %s %gx^%d" % (self.sign(i), abs(self.coefficients[i]), i)
						except OverflowError:
							new_str += " %s %gx^%d" % (self.sign(i), str_long(abs(self.coefficients[i])), i)

		return new_str

	# for ease of use
	def print(self):
		print(self)

	def at(self, x):
		""" return polynomial p(v) at x """
		# using horner's method
		result = 0
		for i in range(len(self.coefficients)-1,-1,-1):
			result = result * x + self.coefficients[i]
		return result

	def dif(self, n=1):
		""" returns the n'th derivative of the polynomial """
		new_poly = Polynomial(self.coefficients[:-n])
		l = len(new_poly.coefficients)
		for i in range(l):
			new_poly.coefficients[i] = mult(self.degree-l+i+2-n, n) * self.coefficients[i+n]
		
		return new_poly


	# can call polynomial by p(x)
	__call__ = at



	@property
	def degree(self):
		return len(self.coefficients) - 1

