import numpy as np

a = np.arange(101)
print(">>> ",a)
np.save("save_a", a)
b = np.load("save_a.npy")
print(">>> ",b)
