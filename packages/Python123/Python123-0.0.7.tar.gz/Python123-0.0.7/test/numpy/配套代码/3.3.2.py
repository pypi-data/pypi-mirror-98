import numpy as np

x = np.array([4, 3, 6, 7, 4, 2, 5, 6])
y = np.array([1, 1, 0, 0, 1, 1, 0, 0])

print(">>> ", x > 2)
print(">>> ", x == 2)
print(">>> ", x < 2)
print(">>> ", x > y, x == y)
print(">>> ", np.logical_and(x, y))
print("------------------------------------------------------------------------------------------")
print(">>> ", x[x > 5])
x[x == 4] = 99
print(">>> ", x)
x[y == 0] = 0
print(">>> ", x)
print("------------------------------------------------------------------------------------------")
x = np.array([-4, -3, 6, -7, 4, -2, 5, -6])
print(">>> ", np.where(x > 0, 1, -1))
