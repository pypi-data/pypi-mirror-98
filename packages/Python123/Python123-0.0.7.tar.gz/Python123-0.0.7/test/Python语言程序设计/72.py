from Python123 import MessageCommon

m = MessageCommon()

# 72-01-自动轨迹绘制问题分析.mp4
m.检查点(10, "1.自动轨迹绘制问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/2a7fdedb-175de06587f/2a7fdedb-175de06587f.mp4')

# 72-02-自动轨迹绘制实例讲解.mp4
m.检查点(20, "2.自动轨迹绘制实例讲解")
m.视频消息(200, '', 'https://video.python123.io/sv/32a1a7eb-175de065bad/32a1a7eb-175de065bad.mp4')

# 72-03-自动轨迹绘制举一反三.mp4
m.检查点(30, "3.自动轨迹绘制举一反三")
m.视频消息(300, '', 'https://video.python123.io/sv/16bc7c9a-175de065f5f/16bc7c9a-175de065f5f.mp4')

m.生成消息文件(72)
