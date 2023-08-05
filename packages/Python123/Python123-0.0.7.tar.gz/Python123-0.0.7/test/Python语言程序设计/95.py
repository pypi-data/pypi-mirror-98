from Python123 import MessageCommon

m = MessageCommon()

# 95-01-玫瑰花绘制问题分析.mp4
m.检查点(10, "1.玫瑰花绘制问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/8b68beb-175de0727fc/8b68beb-175de0727fc.mp4')

# 95-02-玫瑰花绘制实例展示.mp4
m.检查点(20, "2.玫瑰花绘制实例展示")
m.视频消息(200, '', 'https://video.python123.io/sv/406d7e1b-175de07283d/406d7e1b-175de07283d.mp4')
m.代码消息(201, "", "玫瑰花绘制", "95.1.py", code_type="browser")

# 95-03-玫瑰花绘制举一反三.mp4
m.检查点(30, "3.玫瑰花绘制举一反三")
m.视频消息(300, '', 'https://video.python123.io/sv/570acc6-175de0728a2/570acc6-175de0728a2.mp4')

m.生成消息文件(95)
