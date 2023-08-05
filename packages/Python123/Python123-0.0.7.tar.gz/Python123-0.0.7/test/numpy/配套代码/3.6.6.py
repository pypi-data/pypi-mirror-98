import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
b = a.view()
b = b.reshape(3, 3)
print(">>> ", a)
print(">>> ", b)
print("------------------------------------------------------------------------------------------")
b[1] = 99
print(">>> ", a)
print(">>> ", b)
