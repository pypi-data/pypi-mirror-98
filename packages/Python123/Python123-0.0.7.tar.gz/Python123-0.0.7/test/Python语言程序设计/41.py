from Python123 import MessageCommon

m = MessageCommon()

# 41-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/51358b19-175de052c95/51358b19-175de052c95.mp4')

# 41-02-单分支结构.mp4
m.检查点(20, "2.单分支结构")
m.视频消息(200, '', 'https://video.python123.io/sv/26b56525-175de052da0/26b56525-175de052da0.mp4')
m.代码消息(201, "", "单分支结构", "41.1.py", code_type="browser")

# 41-03-二分支结构.mp4
m.检查点(30, "3.二分支结构")
m.视频消息(300, '', 'https://video.python123.io/sv/5896fd66-175de052df5/5896fd66-175de052df5.mp4')
m.代码消息(301, "", "二分支结构", "41.2.py", code_type="browser")

# 41-04-多分支结构.mp4
m.检查点(40, "4.多分支结构")
m.视频消息(400, '', 'https://video.python123.io/sv/1f8fab64-175de052ec5/1f8fab64-175de052ec5.mp4')
m.代码消息(401, "", "多分支结构", "41.3.py", code_type="browser")

# 41-05-条件判断及组合.mp4
m.检查点(50, "5.条件判断及组合")
m.视频消息(500, '', 'https://video.python123.io/sv/4d1f08b8-175de0537aa/4d1f08b8-175de0537aa.mp4')
m.代码消息(501, "", "条件判断及组合", "41.4.py", code_type="browser")

# 41-06-程序的异常处理.mp4
m.检查点(60, "6.程序的异常处理")
m.视频消息(600, '', 'https://video.python123.io/sv/c55153a-175de053880/c55153a-175de053880.mp4')
m.代码消息(601, "", "异常", "41.5.py", code_type="browser")
m.代码消息(602, "", "异常处理", "41.6.py", code_type="browser")

# 41-07-单元小结.mp4
m.检查点(70, "7.单元小结")
m.视频消息(700, '', 'https://video.python123.io/sv/57edd942-175de0538fd/57edd942-175de0538fd.mp4')

m.生成消息文件(41)
