from Python123 import MessageCommon

m = MessageCommon()

# 74-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/5b451e4b-175de0672fd/5b451e4b-175de0672fd.mp4')

# 74-02-二维数据的表示.mp4
m.检查点(20, "2.二维数据的表示")
m.视频消息(200, '', 'https://video.python123.io/sv/28baf582-175de067377/28baf582-175de067377.mp4')

# 74-03-CSV格式与二维数据的存储.mp4
m.检查点(30, "3.CSV格式与二维数据的存储")
m.视频消息(300, '', 'https://video.python123.io/sv/145d0789-175de0679f4/145d0789-175de0679f4.mp4')

# 74-04-二维数据的处理.mp4
m.检查点(40, "4.二维数据的处理")
m.视频消息(400, '', 'https://video.python123.io/sv/2f3fa6a6-175de067b0f/2f3fa6a6-175de067b0f.mp4')
m.代码消息(401, "", "采用二层循环处理列表", "74.1.py", code_type="browser")

# 74-05-单元小结.mp4
m.检查点(50, "5.单元小结")
m.视频消息(500, '', 'https://video.python123.io/sv/206b65f3-175de067c02/206b65f3-175de067c02.mp4')

m.生成消息文件(74)
