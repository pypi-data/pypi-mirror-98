import numpy as np

a = np.array([1, 2, 3, 4, 5, 7, 8])
print(">>> ", a.dtype)
b = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
print(">>> ", b.dtype)
c = np.array([1, 2, 3, 4, 5, 7, 8], dtype=np.int8)
print(">>> ", c.dtype)
