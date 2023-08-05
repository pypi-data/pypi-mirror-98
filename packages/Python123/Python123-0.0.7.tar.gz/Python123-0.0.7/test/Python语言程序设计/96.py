from Python123 import MessageCommon

m = MessageCommon()

# 96-01-练习与作业.mp4
m.检查点(10, "1.练习与作业")
m.视频消息(100, '', 'https://video.python123.io/sv/356f80be-175de0728ec/356f80be-175de0728ec.mp4')
m.文本消息(101, "", "本周的课程，就到此结束了，感谢你的学习")
m.检查点(20, "2.本周测验")
m.文本消息(999, "", '接下来请前往 <a href="https://python123.io/student/courses/3603/groups/43226/intro">本周测验</a>，检验自己的学习成果！')

m.生成消息文件(96)
