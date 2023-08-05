CurStr = input()
if CurStr[:3] == "RMB":
    c = eval(CurStr[3:]) / 6.78
    print("USD{:.2f}".format(c))
elif CurStr[:3] in ['USD']:
    c = eval(CurStr[3:]) * 6.78
    print("RMB{:.2f}".format(c))
