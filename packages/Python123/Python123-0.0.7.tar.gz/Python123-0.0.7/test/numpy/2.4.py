from Python123 import NMessageCommon

m = NMessageCommon()
m.选择同桌()  # 选择用户  必填
m.文本消息("叮当叮当叮当，开始上课喽。")  # 文本消息  必填
m.文本消息("今天前来和我们一起学习的是【广东佛跳墙大学】")  # 文本消息  必填

# 场景引入
m.文本消息("上一堂课中我们学习了使用 np.array 方法创建数组，或者说把 list 转换为数组对象。")
m.文本消息("如果我们想创建一系列包含规律值的数组时又该怎么办呢？")

# 视频
m.视频消息("https://video.python123.io/sv/5eef0561-1751b6be69a/5eef0561-1751b6be69a.mp4")  # 视频播放地址  必填
m.弹出知识卡(["获得「知识卡」：np.arange", "获得「知识卡」：np.ones", "获得「知识卡」：np.linspace", "获得「知识卡」：np.concatenate",
         "获得「知识卡」：np.random.normal"])
m.弹出知识卡(
    ["获得「知识卡」：np.random.beta", "获得「知识卡」：np.full", "获得「知识卡」：np.eye", "获得「知识卡」：np.ones_like", "获得「知识卡」：np.zeros_like"])
m.课后快速选择题(96947)  # 课后抢答题  必填

# 练习
m.代码消息NumPy("亲自试一试不同的数组创建方法", "2.4.1.py")
m.代码消息NumPy("试一试正态分布数组的创建方法", "2.4.2.py")
m.代码消息NumPy("试一试 Beta 分布数组的创建方法", "2.4.3.py")
m.文本消息("matplotlib 库还为我们提供了很多图表的操作的示例，在后续课程中我们将一一学习。")
m.pk("2.4广东佛跳墙大学", "https://python123.io/iclass/images/numpy/2.4.jpg")
m.课后单选题([104188, 104189, 104190], 30)  # 课后单选题列表  必填
m.生成消息文件(2.4)
