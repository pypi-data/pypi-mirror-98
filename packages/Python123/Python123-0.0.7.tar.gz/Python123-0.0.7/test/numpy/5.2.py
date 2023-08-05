from Python123 import NMessageCommon

m = NMessageCommon()

m.选择同桌()  # 选择用户  必填
m.文本消息("滴滴答答，开始上课了。")  # 文本消息  必填
m.文本消息("今天对手【油爆双脆大学】")  # 文本消息  必填

# 场景引入
m.文本消息("这堂课我们继续学习两个新的 NumPy 方法，也非常常用。")
m.文本消息("当然同时也要继续练习 NumPy 其它方法的使用。")

# 视频
m.视频消息("https://video.python123.io/sv/2c5d56cf-1751b6c3307/2c5d56cf-1751b6c3307.mp4")  # 视频播放地址  必填
m.弹出知识卡(["获得「知识卡」：图片旋转", "获得「知识卡」：图片平移"])
m.课后快速选择题(96963)  # 课后抢答题  必填

# 练习
m.代码消息NumPy_需添加附件("首先打开并查看图片", "5.2.1.py", "lighthouse.jpg")
m.代码消息NumPy_需添加附件("将图片旋转 90 度", "5.2.2.py", "lighthouse.jpg")
m.代码消息NumPy_需添加附件("将图片旋转 270 度", "5.2.3.py", "lighthouse.jpg")
m.代码消息NumPy_需添加附件("「滚动」图片", "5.2.4.py", "lighthouse.jpg")
m.代码消息NumPy_需添加附件("平移图片 - 1", "5.2.5.py", "lighthouse.jpg")
m.代码消息NumPy_需添加附件("平移图片 - 2", "5.2.6.py", "lighthouse.jpg")
m.文本消息("下面开始 PK！别问我油爆双脆是啥，赢了就知道！")  # 文本消息  必填
m.pk("5.2油爆双脆大学", "https://python123.io/iclass/images/numpy/5.2.jpg")
m.课后单选题([101067, 101068], 25)  # 课后单选题列表  必填
m.生成消息文件(5.2)
