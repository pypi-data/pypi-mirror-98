from Python123 import MessageCommon

m = MessageCommon()

# 91-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/1b7dcf6f-175de06edd1/1b7dcf6f-175de06edd1.mp4')

# 91-02-Python库之数据分析.mp4
m.检查点(20, "2.Python库之数据分析")
m.视频消息(200, '', 'https://video.python123.io/sv/13669360-175de06eeba/13669360-175de06eeba.mp4')
m.代码消息(201, "", "Numpy: 表达N维数组的最基础库", "91.1.py")

# 91-03-Python库之数据可视化.mp4
m.检查点(30, "3.Python库之数据可视化")
m.视频消息(300, '', 'https://video.python123.io/sv/32c46625-175de06f51a/32c46625-175de06f51a.mp4')

# 91-04-Python库之文本处理.mp4
m.检查点(40, "4.Python库之文本处理")
m.视频消息(400, '', 'https://video.python123.io/sv/fb3f1d5-175de06f540/fb3f1d5-175de06f540.mp4')

# 91-05-Python库之机器学习.mp4
m.检查点(50, "5.Python库之机器学习")
m.视频消息(500, '', 'https://video.python123.io/sv/12dc5206-175de06f545/12dc5206-175de06f545.mp4')

# 91-06-单元小结.mp4
m.检查点(60, "6.单元小结")
m.视频消息(600, '', 'https://video.python123.io/sv/18043a04-175de06f71f/18043a04-175de06f71f.mp4')

m.生成消息文件(91)
