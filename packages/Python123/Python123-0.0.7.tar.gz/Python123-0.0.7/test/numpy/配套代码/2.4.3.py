import numpy as np
import matplotlib.pyplot as plt

data = np.random.beta(2, 2, 100000)
plt.hist(data, 1000)
plt.show()
