import numpy as np
import matplotlib.pyplot as plt
a = np.random.randint(0,100,200)
np.sort(a)
plt.scatter(range(200), a)
plt.show()