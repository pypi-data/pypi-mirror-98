from Python123 import MessageCommon

m = MessageCommon()

# 76-01-政府工作报告词云问题分析.mp4
m.检查点(10, "1.政府工作报告词云问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/f10461e-175de06874c/f10461e-175de06874c.mp4')

# 76-02-政府工作报告词云实例解析(上).mp4
m.检查点(20, "2.政府工作报告词云实例解析(上)")
m.视频消息(200, '', 'https://video.python123.io/sv/2b6c87c3-175de068896/2b6c87c3-175de068896.mp4')

# 76-03-政府工作报告词云实例解析(下).mp4
m.检查点(30, "3.政府工作报告词云实例解析(下)")
m.视频消息(300, '', 'https://video.python123.io/sv/2b7523de-175de0688f0/2b7523de-175de0688f0.mp4')

m.代码消息附件(301, "", "政府工作报告词云", "76.1.py",
         image="https://python123.io/images/cc/1b/7d07131ba0de5748b469a74b3c2c.png",
         fill="manual",
         attachements_name="新时代中国特色社会主义.txt")

# 76-04-政府工作报告词云举一反三.mp4
m.检查点(40, "4.政府工作报告词云举一反三")
m.视频消息(400, '', 'https://video.python123.io/sv/20e093be-175de068a3d/20e093be-175de068a3d.mp4')

m.文本消息(401, "", '想知道关于词云的原理吗？欢迎浏览 Python123 特别策划：<a target="_blank" href="https://python123.io/tutorials/word_cloud">你不知道的词云</a>')

m.生成消息文件(76)
