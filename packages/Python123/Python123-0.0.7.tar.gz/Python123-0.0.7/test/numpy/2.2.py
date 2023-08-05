from Python123 import NMessageCommon

m = NMessageCommon()
m.选择同桌()  # 选择用户  必填
m.文本消息("咣咣咣，注意了，我们开始上课了。")  # 文本消息  必填
m.文本消息("长话短说，今天的对手是...")  # 文本消息  必填
m.pk("2.2西安肉夹馍大学", "https://python123.io/iclass/images/numpy/2.2.jpg")

# 场景引入
m.文本消息("我们知道 Python 中有整数、浮点数和复数，但 NumPy 却定义了繁多的数据类型，为什么会这样呢？我们来了解下吧~")

# 视频
m.视频消息("https://video.python123.io/sv/5b61c076-1751b6bd4fa/5b61c076-1751b6bd4fa.mp4")  # 视频播放地址  必填
m.弹出知识卡(["获得「知识卡」：数组类型", "获得「知识卡」：数据类型", "获得「知识卡」：ndarray.dtype"])
m.课后快速选择题(96945)  # 课后抢答题  必填

# 练习
m.代码消息NumPy("百看不如一练，动手试试查看不同数组的 dtype", "2.2.py")
m.文本消息("这么多数据类型是不是眼花缭乱，我们需要根据处理的数据的特征，来选择合适的类型。下面就来测验一下吧！")
m.课后单选题([95965, 95968, 95979], 25)  # 课后单选题列表  必填
m.程序设计题(95980)  # 程序设计题
m.生成消息文件(2.2)
