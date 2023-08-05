s = input()
try:
    d = eval(s)
    e = {}
    for k in d:
        dk = d[k]
        print(dk)
        e[dk] = k
    print(e)
except:
    print("输入错误")