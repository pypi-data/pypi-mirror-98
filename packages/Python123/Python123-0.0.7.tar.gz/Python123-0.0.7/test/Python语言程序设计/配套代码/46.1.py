ls = []
for i in range(100, 1000):
    t = str(i)
    if pow(eval(t[0]), 3) + pow(eval(t[1]), 3) + pow(eval(t[2]), 3) == i:
        ls.append(t)
print(",".join(ls))
