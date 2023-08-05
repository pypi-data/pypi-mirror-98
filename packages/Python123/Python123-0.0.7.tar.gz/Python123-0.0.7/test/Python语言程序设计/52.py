from Python123 import MessageCommon

m = MessageCommon()

# 52-01-七段数码管绘制问题分析.mp4
m.检查点(10, "1.七段数码管绘制问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/b96a117-175de058f1e/b96a117-175de058f1e.mp4')

# 52-02-七段数码管绘制实例讲解(上).mp4
m.检查点(20, "2.七段数码管绘制实例讲解(上)")
m.视频消息(200, '', 'https://video.python123.io/sv/309f8d27-175de0596b8/309f8d27-175de0596b8.mp4')

# 52-03-七段数码管绘制实例讲解(下).mp4
m.检查点(30, "3.七段数码管绘制实例讲解(下)")
m.视频消息(300, '', 'https://video.python123.io/sv/3f53daa5-175de05998e/3f53daa5-175de05998e.mp4')

m.文本消息(301, "", "这是一个绘制七段数码管的实例，用于理解函数及其封装的价值")
m.代码消息(302, "", "七段数码管 1 ", "52.1.py",
       image="https://python123.io/images/d5/76/68f14dd175bcf2341fdf946f0693.png",
       fill="manual",
       code_type="browser")

# 52-04-七段数码管绘制举一反三.mp4
m.检查点(40, "4.七段数码管绘制举一反三")
m.视频消息(400, '', 'https://video.python123.io/sv/29129873-175de059ba8/29129873-175de059ba8.mp4')

m.生成消息文件(52)
