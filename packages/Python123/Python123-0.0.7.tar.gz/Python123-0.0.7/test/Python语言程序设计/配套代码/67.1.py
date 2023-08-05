def dev(numbers, mean):  # 计算标准差
    sdev = 0.0
    for num in numbers:
        sdev = sdev + (num - mean) ** 2
    return pow(sdev / (len(numbers) - 1), 0.5)


ls = [1,2,3,4,346,475,73,34,234]

print(dev(ls, sum(ls)/len(ls)))