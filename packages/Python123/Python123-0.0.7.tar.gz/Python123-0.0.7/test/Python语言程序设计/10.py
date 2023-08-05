from Python123 import MessageCommon

m = MessageCommon()

# 10-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.视频消息(100, '', 'https://video.python123.io/sv/854b8b7-175de03f59c/854b8b7-175de03f59c.mp4')

# 10-02-本周概要.mp4
m.检查点(20, "2.本周概要")
m.视频消息(200, '', 'https://video.python123.io/sv/504aa67e-175de03f709/504aa67e-175de03f709.mp4')

m.生成消息文件(10)
