import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(">>> ", np.dot(a, b))
c = np.arange(6).reshape((2, 3))
print(">>> ", c, c.T)
print(">>> ", np.transpose(c))
