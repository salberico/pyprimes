import numpy as np

def isprime(n):
	if n == 2 or n == 3:
		return 1
	if n % 2 == 0 or n % 3 == 0 or n == 1:
		return 0
	i = 5
	w = 2
	while i * i <= n:
		if n % i == 0:
			return 0
		i += w
		w = 6 - w
	return 1
			
def spiral(layers):
	if layers <= 0:
		return []
		
	def getsequence(L):
		return np.concatenate((np.arange(L), np.ones(2*L+1, dtype=np.int64)*L, 
			np.arange(L-1,-L,-1), np.ones(2*L+1, dtype=np.int64)*-L, np.arange(1-L,0)))    
			
	count = 1
	arr = np.ones((layers*2-1,layers*2-1), dtype=np.uint32)
	for layer in range(1, layers):
		sequenceY = getsequence(layer) + layers - 1
		sequenceX = np.roll(sequenceY, -2*layer)
		for x, y in zip(sequenceX, sequenceY):
			count += 1
			arr[x,y] = count
	return arr

	
if __name__ == '__main__':
	import matplotlib.pyplot as plt
	layers = 100
	a = spiral(layers)
	for x in range(layers*2-1):
		for y in range(layers*2-1):
			a[x,y] = isprime(a[x,y])
	plt.figimage(a*255)
	plt.show()

