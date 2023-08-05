import numpy as np

a = np.arange(10)
b = a[0:6]
print(">>> ", a)
print(">>> ", b)
b[1] = 1000
print(">>> ", a)
print(">>> ", b)
print("------------------------------------------------------------------------------------------")
a = list(range(10))
b = a[0:6]
print(">>> ", a)
print(">>> ", b)
b[1] = 1000
print(">>> ", a)
print(">>> ", b)
