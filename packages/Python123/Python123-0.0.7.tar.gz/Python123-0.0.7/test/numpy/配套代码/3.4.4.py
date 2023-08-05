import numpy as np

a = np.random.randint(0, 100, 10)

a.sort()
print(">>> ", a)
print(">>> ", np.searchsorted(a, 5))
print(">>> ", np.insert(a, np.searchsorted(a, 5), 5))
print(">>> ", np.append(a, 100))
print("------------------------------------------------------------------------------------------")
a = np.array([1, 2, 3, 1, 1, 1, 2, 3, 4])
print(">>> ", np.where(a == 1))
a = np.array([0, 1, 0, 2, 0, 2, 0, 3, 0, 4])
print(">>> ", np.count_nonzero(a))
