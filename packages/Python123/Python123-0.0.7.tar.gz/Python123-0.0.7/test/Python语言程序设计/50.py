from Python123 import MessageCommon

m = MessageCommon()


# 50-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.文本消息(98, "", "亲爱的【{name}】，欢迎进入 Python 语言程序设计配套【第 5 周】互动课程")
m.文本消息(99, "", "本周主要讲解函数的概念，包括【函数的基本使用、函数的参数传递、代码复用、基于函数的模块化设计、递归】等，同时介绍标准库【datetime】的使用")
m.视频消息(100, '', 'https://video.python123.io/sv/59250fa6-175de057110/59250fa6-175de057110.mp4')

# 50-02-本课概要.mp4
m.检查点(20, "2.本课概要")
m.视频消息(200, '', 'https://video.python123.io/sv/2ad1b9e7-175de0574db/2ad1b9e7-175de0574db.mp4')

m.生成消息文件(50)
