from Python123 import MessageCommon

m = MessageCommon()

# 60-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.文本消息(98, "", "亲爱的【{name}】，您好，欢迎进入 Python 语言程序设计【第 6 周】互动课程")
m.文本消息(99, "", "本周主要讲解 Python 语言的组合数据类型，包括【元组、集合、列表、字典】等类型的概念和使用，同时，介绍第三方中文分词库【jieba】的使用")
m.视频消息(100, '', 'https://video.python123.io/sv/6f1c883-175de05d991/6f1c883-175de05d991.mp4')

# 60-02-本课概要.mp4
m.检查点(20, "2.本课概要")
m.视频消息(200, '', 'https://video.python123.io/sv/4c4d7dbd-175de05da8d/4c4d7dbd-175de05da8d.mp4')

m.生成消息文件(60)
