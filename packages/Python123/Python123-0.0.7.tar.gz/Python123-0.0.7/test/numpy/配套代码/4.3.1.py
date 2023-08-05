import numpy as np

a = np.random.randint(0, 10, 10)
a = a.reshape(2, 5)
print(">>> ", a)
print(">>> ", np.sort(a))
print(">>> ", np.sort(a, axis=0))
print(">>> ", np.sort(a, axis=1))
