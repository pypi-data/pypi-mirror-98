A = {"p", "y", 123}
for item in A:
    print(item, end="")

#######
try:
    while True:
        print(A.pop(), end="")
except:
    pass
