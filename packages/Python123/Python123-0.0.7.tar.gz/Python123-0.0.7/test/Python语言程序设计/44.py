from Python123 import MessageCommon

m = MessageCommon()

# 44-01-random库基本介绍.mp4
m.检查点(10, "1.random库基本介绍")
m.视频消息(100, '', 'https://video.python123.io/sv/49a2a14-175de05594b/49a2a14-175de05594b.mp4')

# 44-02-基本随机数函数.mp4
m.检查点(20, "2.基本随机数函数")
m.视频消息(200, '', 'https://video.python123.io/sv/34146dc8-175de055e97/34146dc8-175de055e97.mp4')
m.代码消息(201, "", "基本随机数函数 ", "44.1.py")

# 44-03-扩展随机数函数.mp4
m.检查点(30, "3.扩展随机数函数")
m.视频消息(300, '', 'https://video.python123.io/sv/1d8a801b-175de05605a/1d8a801b-175de05605a.mp4')
m.代码消息(301, "", "扩展随机函数 ", "44.2.py")

m.生成消息文件(44)
