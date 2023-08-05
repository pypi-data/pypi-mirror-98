import time
t = time.gmtime()
print(time.strftime("%Y-%m-%d %H:%M:%S", t))

timeStr = '2018-01-26 12:55:20'
print(time.strptime(timeStr, "%Y-%m-%d %H:%M:%S"))
