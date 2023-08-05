from Python123 import MessageCommon

m = MessageCommon()

# 86-01-练习与作业.mp4
m.检查点(10, "1.练习与作业")
m.视频消息(100, '', 'https://video.python123.io/sv/4153cd9-175de06ea6f/4153cd9-175de06ea6f.mp4')
m.文本消息(109, "", "本周的课程，就到此结束了，感谢你的学习")
m.检查点(20, "2.本周测验")
m.文本消息(999, "", '接下来请前往 <a href="https://python123.io/student/courses/3603/groups/43225/intro">本周测验</a>，检验自己的学习成果！')

m.生成消息文件(86)
