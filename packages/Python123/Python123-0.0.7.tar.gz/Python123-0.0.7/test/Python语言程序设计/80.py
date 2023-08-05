from Python123 import MessageCommon

m = MessageCommon()


# 80-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.文本消息(98, "", "亲爱的【{name}】，您好，欢迎进入Python语言程序设计配套【第 8 周】互动课程")
m.文本消息(99, "", "本周主要讲解程序设计方法，包括计算思维、自顶向下、自地向上、Python第三方库安装和使用")
m.视频消息(100, '', 'https://video.python123.io/sv/4bfe5aef-175de0697f4/4bfe5aef-175de0697f4.mp4')

# 80-02-本课概要.mp4
m.检查点(20, "2.本课概要")
m.视频消息(200, '', 'https://video.python123.io/sv/1e3aa9d5-175de06998f/1e3aa9d5-175de06998f.mp4')

m.生成消息文件(80)
