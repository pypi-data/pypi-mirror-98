from Python123 import MessageCommon

m = MessageCommon()

m.文本消息(99, "", "课前提示：本堂课的文件的操作需要同学们在自己电脑上完成练习！")

# 71-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/2cf7863e-175de064077/2cf7863e-175de064077.mp4')

# 71-02-文件的类型.mp4
m.检查点(20, "2.文件的类型")
m.视频消息(200, '', 'https://video.python123.io/sv/10ae71cd-175de0640c7/10ae71cd-175de0640c7.mp4')

# 71-03-文件的打开和关闭.mp4
m.检查点(30, "3.文件的打开和关闭")
m.视频消息(300, '', 'https://video.python123.io/sv/e52593-175de0642c0/e52593-175de0642c0.mp4')

# 71-04-文件内容的读取.mp4
m.检查点(40, "4.文件内容的读取")
m.视频消息(400, '', 'https://video.python123.io/sv/5b4363f4-175de064a19/5b4363f4-175de064a19.mp4')

# 71-05-数据的文件写入.mp4
m.检查点(50, "5.数据的文件写入")
m.视频消息(500, '', 'https://video.python123.io/sv/12a45c8d-175de064a3e/12a45c8d-175de064a3e.mp4')

# 71-06-单元小结.mp4
m.检查点(60, "6.单元小结")
m.视频消息(600, '', 'https://video.python123.io/sv/4218b42a-175de064a60/4218b42a-175de064a60.mp4')

m.生成消息文件(71)
