from Python123 import MessageCommon

m = MessageCommon()

# 70-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.文本消息(98, "", "亲爱的【{name}】，您好，欢迎进入 Python 语言程序设计【第 7 周】互动课程")
m.文本消息(99, "", "本周主要讲解文件和数据格式化，包括文件的使用以及以一二维和高维数据组织和格式化方法，介绍第三方图像处理库 PIL 和标准库 json 的使用")
m.视频消息(100, '', 'https://video.python123.io/sv/145ae7f1-175de063c13/145ae7f1-175de063c13.mp4')

# 70-02-本课概要.mp4
m.检查点(20, "2.本课概要")
m.视频消息(200, '', 'https://video.python123.io/sv/5595fec8-175de063f6f/5595fec8-175de063f6f.mp4')

m.生成消息文件(70)
