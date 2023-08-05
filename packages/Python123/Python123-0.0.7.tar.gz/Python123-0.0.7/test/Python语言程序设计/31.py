from Python123 import MessageCommon

m = MessageCommon()

# 31-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/2b8fe122-175de04ad2d/2b8fe122-175de04ad2d.mp4')

# 31-02-整数类型.mp4
m.检查点(20, "2.整数类型")
m.视频消息(200, '', 'https://video.python123.io/sv/226897a1-175de04aea8/226897a1-175de04aea8.mp4')

m.代码消息(201, "", "无限制整数", "31.1.py")

# 31-03-浮点数类型.mp4
m.检查点(30, "3.浮点数类型")
m.视频消息(300, '', 'https://video.python123.io/sv/21363063-175de04b094/21363063-175de04b094.mp4')

m.代码消息(301, "", "浮点数间运算存在不确定尾数，不是 bug", "31.2.py")

# 31-04-复数类型.mp4
m.检查点(40, "4.复数类型")
m.视频消息(400, '', 'https://video.python123.io/sv/1df4053c-175de04b9d2/1df4053c-175de04b9d2.mp4')

# 31-05-数值运算操作符.mp4
m.检查点(50, "5.数值运算操作符")
m.视频消息(500, '', 'https://video.python123.io/sv/1f569f50-175de04ba82/1f569f50-175de04ba82.mp4')

# 31-06-数值运算函数.mp4
m.检查点(60, "6.数值运算函数")
m.视频消息(600, '', 'https://video.python123.io/sv/574abc0f-175de04bca1/574abc0f-175de04bca1.mp4')

# 31-07-单元小结.mp4
m.检查点(70, "7.单元小结")
m.视频消息(700, '', 'https://video.python123.io/sv/bca323-175de04be29/bca323-175de04be29.mp4')

m.生成消息文件(31)
