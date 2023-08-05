from Python123 import MessageCommon

m = MessageCommon()

# 33-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/2c73addf-175de04d8e5/2c73addf-175de04d8e5.mp4')

# 33-02-字符串类型的表示.mp4
m.检查点(20, "2.字符串类型的表示")
m.视频消息(200, '', 'https://video.python123.io/sv/47b17e72-175de04dcb1/47b17e72-175de04dcb1.mp4')

# 33-03-字符串操作符.mp4
m.检查点(30, "3.字符串操作符")
m.视频消息(300, '', 'https://video.python123.io/sv/2a8ccf22-175de04e5de/2a8ccf22-175de04e5de.mp4')

m.代码消息(301, "", "获取星期字符串", "33.1.py", code_type="browser")
m.代码消息(302, "", "获取星期字符串 V2", "33.2.py", code_type="browser")

# 33-04-字符串处理函数.mp4
m.检查点(40, "4.字符串处理函数")
m.视频消息(400, '', 'https://video.python123.io/sv/53cd5d15-175de04e7b5/53cd5d15-175de04e7b5.mp4')
m.代码消息(401, "", "Unicode编码", "33.3.py")

# 33-05-字符串处理方法.mp4
m.检查点(50, "5.字符串处理方法")
m.视频消息(500, '', 'https://video.python123.io/sv/4b3cafbe-175de04e7e8/4b3cafbe-175de04e7e8.mp4')

# 33-06-字符串类型的格式化.mp4
m.检查点(60, "6.字符串类型的格式化")
m.视频消息(600, '', 'https://video.python123.io/sv/49521d0e-175de04e80f/49521d0e-175de04e80f.mp4')
m.代码消息(601, "", "字符串类型的格式化", "33.4.py")

# 33-07-单元小结.mp4
m.检查点(70, "7.单元小结")
m.视频消息(700, '', 'https://video.python123.io/sv/2cc8d8b3-175de04fc0e/2cc8d8b3-175de04fc0e.mp4')

m.生成消息文件(33)
