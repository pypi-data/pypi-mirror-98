import numpy as np
import sys

ls = list(range(100000))
a = np.array(ls)
print(">>> ", a.dtype)
print(">>> ", a.ndim)
print(">>> ", a.shape)
print(">>> ", a.size)
print(">>> ", len(a))
print(">>> ", a.itemsize)
print(">>> ", a.itemsize * a.size)
print(">>> ", sys.getsizeof(a))
print(">>> ", sys.getsizeof(ls))
