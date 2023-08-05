import numpy as np
import matplotlib.pyplot as plt

a = np.arange(10)
print(">>> ", a)
print(">>> ", np.arange(0.1, 2.0, 0.1))
print(">>> ", np.ones(10))
print("------------------------------------------------------------------------------------------")
print(">>> ", np.ones((3, 3)))
print(">>> ", np.zeros(8))
print("------------------------------------------------------------------------------------------")
print(">>> ", np.linspace(1, 2))
print(">>> ", np.linspace(1, 2, endpoint=False))
print("------------------------------------------------------------------------------------------")
print(">>> ", np.linspace(1, 2, num=5))

x1 = np.linspace(0, 1, num=10)
x2 = np.linspace(1, 2, num=10)
y = np.zeros(10)

plt.plot(x1, y, "o")
plt.plot(x2, y, "o")
plt.show()
