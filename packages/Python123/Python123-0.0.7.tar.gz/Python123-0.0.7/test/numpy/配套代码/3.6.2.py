import numpy as np

a = np.array(11)
b = np.ones(11)
print(">>> ",a, b)
np.savez("save_ab", a, b)
save_ab_npz = np.load("save_ab.npz")
print(">>> ",save_ab_npz)
print(">>> ",save_ab_npz["arr_0"])
print(">>> ",save_ab_npz["arr_1"])
