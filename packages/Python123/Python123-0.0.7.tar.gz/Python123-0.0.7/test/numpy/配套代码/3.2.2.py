import numpy as np


a = np.arange(10)
b = np.arange(10)
print(">>> ", a, b)
c = np.ones(10)
d = np.add(a, b, out=c)
print(">>> ", c)
print(">>> ", id(c), id(d))

print("------------------------------------------------------------------------------------------")
a = np.array([3, 5, 2, 5, 7, 4, 7, 0])
b = np.array([0, 9, 0, 9, 0, 9, 0, 9])
print(">>> ", np.maximum(a, b))

print("------------------------------------------------------------------------------------------")
a = np.array([3, 5, 2, 5, 7, 4, 7, 0])
b = np.array([0, 9, 0, 9, 0, 9, 0, 9])
c = np.greater(a, b)
print(">>> ", c)
print(">>> ", a[c])
