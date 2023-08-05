from Python123 import MessageCommon

m = MessageCommon()

# 40-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.文本消息(98, "", "亲爱的【{name}】，欢迎进入 Python 语言程序设计【第 5 周】互动课程")
m.文本消息(99, "", "本周主要讲解 Python 语言的指令控制结构，包括【顺序结构、分支结构、循环结构、异常处理结构】等，同时介绍标准库【random】的使用")
m.视频消息(100, '', 'https://video.python123.io/sv/51e38e9b-175de051e91/51e38e9b-175de051e91.mp4')

# 40-02-本课概要.mp4
m.检查点(20, "2.本课概要")
m.视频消息(200, '', 'https://video.python123.io/sv/368b8374-175de052c37/368b8374-175de052c37.mp4')

m.生成消息文件(40)
