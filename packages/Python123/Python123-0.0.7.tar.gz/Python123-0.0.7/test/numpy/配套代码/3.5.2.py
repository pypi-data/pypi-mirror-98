import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
print(">>> ", a)
print(">>> ", np.cumsum(a))
print(">>> ", np.cumprod(a))
print("------------------------------------------------------------------------------------------")
a = np.random.randint(0, 10, 100)
print(">>> ", np.unique(a))
print("------------------------------------------------------------------------------------------")
a = np.random.randint(0, 10, 10)
b = np.random.randint(5, 15, 10)
print(">>> ", a, b)
print(">>> ", np.intersect1d(a, b))
print(">>> ", np.union1d(a, b))
print(">>> ", np.in1d(a, b))
print(">>> ", np.setdiff1d(a, b))
print(">>> ", np.setxor1d(a, b))
