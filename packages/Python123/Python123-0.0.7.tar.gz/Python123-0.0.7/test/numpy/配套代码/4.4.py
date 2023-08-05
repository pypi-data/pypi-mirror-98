import numpy as np

t = np.array([
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14, 15, 16, 17, 18],
    [19, 20, 21, 22, 23, 24, 25, 26, 27], ])
print(">>> ", np.mean(t))
print(">>> ", np.mean(t, axis=0))
avg = np.sum(t, axis=1)
print(">>> ", np.max(avg), np.min(avg))
a = np.array([[8, 1, 1], [2, 0, 2], [2, 0, 2]])
print(">>> ", np.unique(a))
print(">>> ", np.unique(a, axis=1))
print(">>> ", np.unique(a, axis=0))
