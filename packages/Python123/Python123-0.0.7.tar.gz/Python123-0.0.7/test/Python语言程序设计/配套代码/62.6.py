ls = ["cat", "dog", "tiger", 1024]
ls[1:2] = [1, 2, 3, 4]
print(ls[1:2])

del ls[::3]
print(ls)

ls * 2
print(ls)
