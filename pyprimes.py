def isprime(n):
	"""
	Simple primality test based on the fact
	that other than 2 and 3 all primes are in the form 6i +- 1
	through optimized trial division.
	"""
	# Handle edge cases
	if n == 2 or n == 3:
		return True
	if n % 2 == 0 or n % 3 == 0 or n == 1:
		return False

	fac = 5
	inc = 2

	while fac * fac <= n:
		if n % fac == 0:
			return False

		# increment is either 4 or 2 therefore holding the for 6i +- 1 for increment
		fac += inc

		# Flip flop increment from 4 to 2
		inc = 6 - inc

	return True

def factorize(n):
	"""
	Basic prime factorization with small optimizations.
	Tried with 6n +- 1 from isprime() but saw unexpected slowdowns
	"""
	out = []
	def reduce(x):
		if x > 2:
			# Check the two case, since it's not included later on
			if x % 2 == 0:
				out.append(2), reduce(x//2)
				return

			# Check odd factors
			for factor in range(3,int(x**0.5+1),2):
				if x % factor == 0:
					# Further factor the results
					reduce(factor), reduce(x//factor)
					return

		# Will be prime if this is reached
		out.append(x)

	# Start recursion
	reduce(n)
	return out

def miller_rabin(n):
	"""
	Basic miller rabin primality test:
	https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
	"""
	from random import randint

	# Instant composites
	if n % 2 == 0:
		if n == 2:
			return True
		return False
	if n < 2:
		return False

	# n−1 as 2**r·d
	bnless = bin(n-1)
	# r is how many times n-1 is divisible by 2
	# view in binary then count ending zeros
	r = len(bnless) - len(bnless.rstrip('0'))
	d = n//2**r

	# Mainloop
	for a in [2,3,5]:
		a = randint(2, n-2)
		x = a**d % n
		if x == 1 or x == n - 1:
			continue
		for _ in range(r-1):
			x = x**2 % n
			if x == 1:
				return False
			if x == n - 1:
				break
		else:
			return False
	return True

def gcd(x, y):
	"""
	Recursive Euclidean Algorithm, for calculating 'Greatest Common Denominator'(GCD)
	"""
	if not x:
		return y
	else:
		return gcd(x, y%x)

def sieve(n):
	"""
	Memory inefficient simple sieve of eratosthenes for prime generation up to n
	still decently quick but can still be optimized greatly.
	"""
	
	# Edge case handling
	if n < 2:
		return []
	if n == 2:
		return [2]
		
	# Initialize base number list
	numbers = [2] + list(range(3,n+1,2))
	index = 1
	increment = numbers[index]
	
	# Store calculations which are reused
	t_count = len(numbers)
	t_root = n**0.5+1
	
	while increment < t_root:
		# 'Removing' (making zero) numbers which are multiples of current increment
		# since the list is in order just have to count by the said increment
		for remove_index in range(index+increment, t_count, increment):
			numbers[remove_index] = 0

		# Get next non-zero increment, which will be a prime at this point
		for candidate_index in range(index+1, t_count):
			if numbers[candidate_index] != 0:
				index = candidate_index
				increment = numbers[index]
				break
				
	# Return only the non-zero numbers which are proven primes
	return [number for number in numbers if number != 0]
	
def spiral(layers):
	"""
	Generate numpy array of spiraled numbers starting from the center
	can be used to show the patterns in primes
	"""
	import numpy as np

	if layers <= 0:
		return []

	# Get sequence of indices which are to be used at the said layer offset from the center
	def getsequence(L):
		return np.concatenate((np.arange(L), np.ones(2*L+1, dtype=np.int64)*L,
			np.arange(L-1,-L,-1), np.ones(2*L+1, dtype=np.int64)*-L, np.arange(1-L,0)))

	count = 1
	arr = np.ones((layers*2-1,layers*2-1), dtype=np.uint32)
	for layer in range(1, layers):

		# Generate the Y indices for the layer and offset based on the center coordinates
		sequenceY = getsequence(layer) + layers - 1

		# Offset X indices from the generated Y
		sequenceX = np.roll(sequenceY, -2*layer)

		# Assign incremental values to the indices in order
		for x, y in zip(sequenceX, sequenceY):
			count += 1
			arr[x,y] = count

	return arr

if __name__ == '__main__':
	# Testing
	import matplotlib.pyplot as plt
	layers = 100
	a = spiral(layers)
	for x in range(layers*2-1):
		for y in range(layers*2-1):
			a[x,y] = isprime(a[x,y])
	plt.figimage(a*255)
	plt.show()
