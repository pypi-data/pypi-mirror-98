import numpy as np

a = np.arange(100).reshape(10, 10)
np.savetxt("arange.csv", a)
np.savetxt("arange1.csv", a, fmt="%d")
np.savetxt("arange2.csv", a, fmt="%d", delimiter=",")
np.savetxt("arange3.csv", a, fmt="%d", delimiter=",", newline="===\n")
print(">>> ",np.loadtxt("arange2.csv", delimiter=","))
