import time
import numpy as np

# 生成数据
ls = []
for i in range(1000000):
    ls.append(i)

star = time.time()
sum(ls)  # 使用Python内置函数求和
end = time.time()
print("列表计算用时{}".format(end - star))

a = np.array(ls, dtype=np.int64)  # 创建nd.array数组
star = time.time()
np.sum(a)  # 使用numpy内置函数求和
end = time.time()
print("数组计算用时{}".format(end - star))
