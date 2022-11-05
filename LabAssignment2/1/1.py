import numpy as np

M = np.array(list(range(5,21)))
print(M)
print()

M = M.reshape(4,4)
print(M)
print()

M[1:3,1:3] = 0
print(M)
print()

M = M@M
print(M)
print()

v = M[0]
sqrt = np.sqrt(v@v)
print(sqrt)