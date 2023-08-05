from Python123 import NMessageCommon

m = NMessageCommon()
m.选择同桌()  # 选择用户  必填
m.文本消息("滴滴滴，滴滴滴，开始上课了。")  # 文本消息  必填
m.文本消息("今天前来踢馆的是【煎饼卷大葱大学】！")  # 文本消息  必填

# 场景引入
m.文本消息("前面的课程算是开胃小菜，这堂课我们终于要进入 NumPy 核心知识点的学习了。")
m.文本消息("NumPy 的强大之处在于它为我们提供了丰富且快速的元素运算函数。学会这些方法，可以大大简化我们的数据分析编码难度。")

# 视频
m.视频消息("https://video.python123.io/sv/23b1307-1751b6be836/23b1307-1751b6be836.mp4")  # 视频播放地址  必填
m.弹出知识卡(["获得「知识卡」：np.abs", "获得「知识卡」：np.sqrt", "获得「知识卡」：np.floor", "获得「知识卡」：np.rint", "获得「知识卡」np.cos"])
m.弹出知识卡(["获得「知识卡」：np.max", "获得「知识卡」：np.add", "获得「知识卡」：np.subtract", "获得「知识卡」：np.divide", "获得「知识卡」np.greater"])
m.课后快速选择题(96950)  # 课后抢答题  必填


# 练习
m.代码消息NumPy("一元通用函数的练习", "3.2.1.py")
m.代码消息NumPy("二元通用函数的练习", "3.2.2.py")

m.文本消息("对战考试，马上开始")  # 文本消息  必填
m.pk("3.2煎饼卷大葱大学", "https://python123.io/iclass/images/numpy/3.2.jpg")
m.课后单选题([104196, 104796, 104797],60)  # 课后单选题列表  必填
m.程序设计题(104195)  # 程序设计题
m.生成消息文件(3.2)
