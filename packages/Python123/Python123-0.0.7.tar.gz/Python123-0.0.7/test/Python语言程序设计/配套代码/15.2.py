import keyword

print("当前解释器关键字有{}个,分别是：".format(len(keyword.kwlist)))
for i in keyword.kwlist:
    print(i)
