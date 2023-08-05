import numpy as np

a = np.arange(101)
print(">>> ", a)
print(">>> ", np.sum(a))
print(">>> ", np.mean(a))
print(">>> ", np.std(a))
print("------------------------------------------------------------------------------------------")
a = np.array([80, 67, 61])
print(">>> ", np.average(a))
print(">>> ", np.mean(a))
weight = [60, 20, 20]
print(">>> ", np.average(a, weights=weight))
