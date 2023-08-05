from Python123 import MessageCommon

m = MessageCommon()

# 43-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/4c48219b-175de054734/4c48219b-175de054734.mp4')

# 43-02-遍历循环.mp4
m.检查点(20, "2.遍历循环")
m.视频消息(200, '', 'https://video.python123.io/sv/9a1a9b0-175de054983/9a1a9b0-175de054983.mp4')

# 43-03-无限循环.mp4
m.检查点(30, "3.无限循环")
m.视频消息(300, '', 'https://video.python123.io/sv/28bc9ff6-175de0549c2/28bc9ff6-175de0549c2.mp4')

# 43-04-循环控制保留字.mp4
m.检查点(40, "4.循环控制保留字")
m.视频消息(400, '', 'https://video.python123.io/sv/58cf7312-175de054a6a/58cf7312-175de054a6a.mp4')

# 43-05-循环的高级用法.mp4
m.检查点(50, "5.循环的高级用法")
m.视频消息(500, '', 'https://video.python123.io/sv/22ee8a43-175de054c03/22ee8a43-175de054c03.mp4')
m.代码消息(501, "", "循环的高级用法", "43.1.py", code_type="browser")

# 43-06-单元小结.mp4
m.检查点(60, "6.单元小结")
m.视频消息(600, '', 'https://video.python123.io/sv/306944ba-175de054fe3/306944ba-175de054fe3.mp4')

m.生成消息文件(43)
