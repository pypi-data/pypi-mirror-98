import numpy as np

c = np.zeros(11)
d = np.ones(11)
print(">>> ",c, d)

np.savez("save_cd", int_c=c, float_d=d)
save_cd_npz = np.load("save_cd.npz")
print(">>> ",save_cd_npz)
print(">>> ",save_cd_npz["int_c"], save_cd_npz["float_d"])
