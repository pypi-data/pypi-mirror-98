from Python123 import MessageCommon

m = MessageCommon()

# 65-01-jieba库基本介绍.mp4
m.检查点(10, "1.jieba库基本介绍")
m.视频消息(100, '', 'https://video.python123.io/sv/5cf33618-175de061bd8/5cf33618-175de061bd8.mp4')

# 65-02-jieba库使用说明.mp4
m.检查点(20, "2.jieba库使用说明")
m.视频消息(200, '', 'https://video.python123.io/sv/222202c8-175de062674/222202c8-175de062674.mp4')

m.文本消息(201, '', '我们将在下一节中使用 jieba 库完成《三国演义》的人物出场统计')

m.生成消息文件(65)
