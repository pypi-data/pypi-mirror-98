from Python123 import MessageCommon

m = MessageCommon()

# 34-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/2f3aef1e-175de04fd80/2f3aef1e-175de04fd80.mp4')

# 34-02-time库基本介绍.mp4
m.检查点(20, "2.time库基本介绍")
m.视频消息(200, '', 'https://video.python123.io/sv/1ec6aba2-175de0500a8/1ec6aba2-175de0500a8.mp4')

# 34-03-时间获取.mp4
m.检查点(30, "3.时间获取")
m.视频消息(300, '', 'https://video.python123.io/sv/3f327dbb-175de050107/3f327dbb-175de050107.mp4')

# 34-04-时间格式化.mp4
m.检查点(40, "4.时间格式化")
m.视频消息(400, '', 'https://video.python123.io/sv/5c9b0f43-175de05064f/5c9b0f43-175de05064f.mp4')
m.代码消息(401, "", "时间格式化", "34.1.py")

# 34-05-程序计时应用.mp4
m.检查点(50, "5.程序计时应用")
m.视频消息(500, '', 'https://video.python123.io/sv/17569858-175de0507b4/17569858-175de0507b4.mp4')

# 34-06-单元小结.mp4
m.检查点(60, "6.单元小结")
m.视频消息(600, '', 'https://video.python123.io/sv/59ca8ec4-175de050940/59ca8ec4-175de050940.mp4')

m.生成消息文件(34)
