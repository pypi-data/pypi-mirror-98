import time

print(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time())))
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
