import numpy as np
import matplotlib.pyplot as plt

a = np.arange(0, 10)
b = np.arange(10, 20)
print(">>> ", np.concatenate((a, b)))

data = np.random.normal(2, 0.1, 100000)
plt.hist(data, 1000)
plt.show()
