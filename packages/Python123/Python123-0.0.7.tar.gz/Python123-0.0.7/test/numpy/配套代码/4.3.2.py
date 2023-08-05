import numpy as np

t = np.array([
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14, 15, 16, 17, 18],
    [19, 20, 21, 22, 23, 24, 25, 26, 27], ])
print(">>> ", np.sort(t))
print(">>> ", np.sort(t, axis=0))
print(">>> ", np.sort(t, axis=None))
print(">>> ", np.where(t == 10))
print(">>> ", t[1, 6], t[2, 6])
print(">>> ", t[np.where(t > 10)])
