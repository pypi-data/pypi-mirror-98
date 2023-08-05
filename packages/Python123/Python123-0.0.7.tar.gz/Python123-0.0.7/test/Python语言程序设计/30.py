from Python123 import MessageCommon

m = MessageCommon()


# 30-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.文本消息(101, "", "亲爱的【{name}】，您好，欢迎进入Python语言程序设计【第 3 周】互动课程")
m.文本消息(102, "", "本周主要讲解 Python 语言的基本数据类型，包括【整数、浮点数、复数，字符串】等类型的概念和使用。")
m.视频消息(100, '', 'https://video.python123.io/sv/26d0a5e9-175de04a7f9/26d0a5e9-175de04a7f9.mp4')

# 30-02-本课概要.mp4
m.检查点(20, "2.本课概要")
m.视频消息(200, '', 'https://video.python123.io/sv/242d5d9d-175de04ab9d/242d5d9d-175de04ab9d.mp4')

m.生成消息文件(30)
