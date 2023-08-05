from Python123 import MessageCommon

m = MessageCommon()

# 45-01-圆周率的计算问题分析.mp4
m.检查点(10, "1.圆周率的计算问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/27990f78-175de056227/27990f78-175de056227.mp4')

# 45-02-圆周率的计算实例讲解.mp4
m.检查点(20, "2.圆周率的计算实例讲解")
m.视频消息(200, '', 'https://video.python123.io/sv/472c5d61-175de056274/472c5d61-175de056274.mp4')

m.代码消息(201, "", "π值计算 1", "45.1.py",
       image="https://python123.io/images/87/d9/d71fdb47507a7188a67f90fe426a.png",
       fill="manual")

m.代码消息(202, "", "π值计算 2", "45.2.py",
       image="https://python123.io/images/14/c8/8af1d4c034739a34755647fa4944.png",
       fill="manual")

m.代码消息(203, "", "π值计算 3", "45.3.py", code_type="browser")

m.文本消息(1121, "", "三套【π值计算】训练下来，是不是已经很有成就感了呢？")

# 45-03-圆周率的计算举一反三.mp4
m.检查点(30, "3.圆周率的计算举一反三")
m.视频消息(300, '', 'https://video.python123.io/sv/40760a50-175de0566ef/40760a50-175de0566ef.mp4')

m.生成消息文件(45)
