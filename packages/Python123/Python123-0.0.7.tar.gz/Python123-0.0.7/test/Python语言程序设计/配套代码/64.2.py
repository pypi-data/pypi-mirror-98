d = {"中国": "北京", "美国": "华盛顿", "法国": "巴黎"}
print(d.get("中国", "伊斯兰堡"))
print(d.get("巴基斯坦", "伊斯兰堡"))
d.popitem()
print(d)
