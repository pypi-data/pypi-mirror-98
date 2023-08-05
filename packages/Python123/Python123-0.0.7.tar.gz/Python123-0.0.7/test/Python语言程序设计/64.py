from Python123 import MessageCommon

m = MessageCommon()

# 64-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/3af891a8-175de060e35/3af891a8-175de060e35.mp4')

# 64-02-字典类型定义.mp4
m.检查点(20, "2.字典类型定义")
m.视频消息(200, '', 'https://video.python123.io/sv/4f9bca26-175de06155e/4f9bca26-175de06155e.mp4')

# 64-03-字典处理函数及方法.mp4
m.检查点(30, "3.字典处理函数及方法")
m.视频消息(300, '', 'https://video.python123.io/sv/36d1ea69-175de0616ec/36d1ea69-175de0616ec.mp4')
m.代码消息(301, "", "字典处理函数及方法", "64.1.py")

# 64-04-字典类型应用场景.mp4
m.检查点(40, "4.字典类型应用场景")
m.视频消息(400, '', 'https://video.python123.io/sv/c0cbf97-175de0618fe/c0cbf97-175de0618fe.mp4')
m.代码消息(401, "", "字典类型应用操作", "64.2.py")

# 64-05-单元小结.mp4
m.检查点(50, "5.单元小结")
m.视频消息(500, '', 'https://video.python123.io/sv/7fac8ce-175de061a05/7fac8ce-175de061a05.mp4')

m.生成消息文件(64)
