from Python123 import MessageCommon

m = MessageCommon()

# 20-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.视频消息(100, '', 'https://video.python123.io/sv/28560c41-175de044e91/28560c41-175de044e91.mp4')

# 20-02-本课概要.mp4
m.检查点(20, "2.本课概要")
m.视频消息(200, '', 'https://video.python123.io/sv/5f2a6bd4-175de0452eb/5f2a6bd4-175de0452eb.mp4')

m.生成消息文件(20)
