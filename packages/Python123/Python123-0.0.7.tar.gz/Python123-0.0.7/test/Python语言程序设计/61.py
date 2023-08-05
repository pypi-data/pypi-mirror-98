from Python123 import MessageCommon

m = MessageCommon()

# 61-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/48588acf-175de05dbf1/48588acf-175de05dbf1.mp4')

# 61-02-集合类型定义.mp4
m.检查点(20, "2.集合类型定义")
m.视频消息(200, '', 'https://video.python123.io/sv/49de381f-175de05dc4a/49de381f-175de05dc4a.mp4')
m.代码消息(201, "", "集合类型定义", "61.1.py")

# 61-03-集合操作符.mp4
m.检查点(30, "3.集合操作符")
m.视频消息(300, '', 'https://video.python123.io/sv/42e07b24-175de05e090/42e07b24-175de05e090.mp4')
m.代码消息(301, "", "集合操作符", "61.2.py")

# 61-04-集合处理方法.mp4
m.检查点(40, "4.集合处理方法")
m.视频消息(400, '', 'https://video.python123.io/sv/5750cef5-175de05e66b/5750cef5-175de05e66b.mp4')
m.代码消息(401, "", "集合处理方法", "61.3.py")

# 61-05-集合类型应用场景.mp4
m.检查点(50, "5.集合类型应用场景")
m.视频消息(500, '', 'https://video.python123.io/sv/3b11da85-175de05e6c3/3b11da85-175de05e6c3.mp4')
m.代码消息(501, "", "包含关系比较", "61.4.py")
m.代码消息(502, "", "数据去重", "61.5.py")

# 61-06-单元小结.mp4
m.检查点(60, "6.单元小结")
m.视频消息(600, '', 'https://video.python123.io/sv/42e43b7a-175de05e77b/42e43b7a-175de05e77b.mp4')

m.生成消息文件(61)
