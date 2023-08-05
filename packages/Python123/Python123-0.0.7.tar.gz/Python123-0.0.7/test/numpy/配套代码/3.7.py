import numpy as np

a = np.array([
    ('小明', 28, 65.0), ('小王', 24, 74.0)],
    dtype=[('name', 'U10'), ('age', 'i4'), ('weight', 'f4')])
print(">>> ", a.dtype)
print(">>> ", a)
print(">>> ", a[0])
print(">>> ", a["age"])
print(">>> ", a["name"])
