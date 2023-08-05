TempStr = input("请输入一个带有符号的温度值(82F)：")
if TempStr[-1] in ['C', 'c']:
    f = (eval(TempStr[:-1])) * 1.8 + 32
    print("{:.2f}F".format(f))
elif TempStr[-1] in ['F', 'f']:
    c = (eval(TempStr[:-1]) - 32) / 1.8
    print("{:.2f}C".format(c))
