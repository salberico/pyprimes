import numpy as np
import matplotlib.pyplot as plt

def getsequence(L):
    return np.concatenate((np.arange(L), np.ones(2*L+1, dtype=np.int64)*L, 
        np.arange(L-1,-L,-1), np.ones(2*L+1, dtype=np.int64)*-L, np.arange(1-L,0)))    

def isprime(n):
    if n == 2 or n == 3:
        return 0
    if n % 2 == 0 or n % 3 == 0 or n == 1:
        return 0
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return 1
        i += w
        w = 6 - w
    return 1

def genspiral(layers):
    count = 0
    arr = np.zeros((layers*2-1,layers*2-1,3))
    for layer in range(layers):
        sequenceY = getsequence(layer)
        sequenceX = np.roll(sequenceY, -2*layer)
        for i in range(len(sequenceY)):
            count += 1
            arr[sequenceX[i]+layers-1,sequenceY[i]+layers-1] = ((arr.size/arr.shape[-1]),(arr.size/arr.shape[-1]),(arr.size/arr.shape[-1]))#(count, count, count)
            if isprime(count):
                 arr[sequenceX[i]+layers-1,sequenceY[i]+layers-1] = ((arr.size/arr.shape[-1]), 0, (arr.size/arr.shape[-1]))           
    return arr

if __name__ == '__main__':
    a = genspiral(400)
    plt.figimage(np.uint(a * 255/(a.size/a.shape[-1]))+1)
    plt.show()


