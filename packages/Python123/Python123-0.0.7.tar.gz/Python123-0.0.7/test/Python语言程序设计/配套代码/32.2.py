dayfactor = 0.01
dayup = pow(1 + dayfactor, 365)
daydown = pow(1 - dayfactor, 365)
print("天天向上：{:.2f}, 天天向下：{:.2f}".format(dayup, daydown))
