import numpy as np

a = np.arange(10)
print(">>> ", a)
b = [True, True, False, False, False, True, True, False, False, False]
print(">>> ", a[b])
print("------------------------------------------------------------------------------------------")
a = np.arange(10)
print(">>> ", a)
print(">>> ", a[1:4])
print(">>> ", a[0:6:2])
