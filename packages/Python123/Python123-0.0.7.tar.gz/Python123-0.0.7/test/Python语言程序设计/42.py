from Python123 import MessageCommon

m = MessageCommon()

# 42-01-身体质量指数BMI问题分析.mp4
m.检查点(10, "1.身体质量指数BMI问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/cf5fecb-175de05394d/cf5fecb-175de05394d.mp4')

# 42-02-身体质量指数BMI实例讲解.mp4
m.检查点(20, "2.身体质量指数BMI实例讲解")
m.视频消息(200, '', 'https://video.python123.io/sv/18e83e13-175de0539cf/18e83e13-175de0539cf.mp4')
m.文本消息(201, "", "先对照着敲一遍右侧课件中的代码【身体质量指标BMI 1】")
m.代码消息(202, "", "身体质量指数BMI 1 ", "42.1.py",
       image="https://python123.io/images/36/fa/4f5e44b38d04066fca97b17d1538.png",
       fill="manual",
       code_type="browser")

m.文本消息(203, "", "我们再来练习敲一遍右侧课件中的代码【身体质量指标BMI 2】")
m.代码消息(204, "", "身体质量指数BMI 2 ", "42.2.py",
       image="https://python123.io/images/73/35/1cc19b0025c2ad5f2c4de2a77115.png",
       fill="manual",
       code_type="browser")

m.文本消息(205, "", "再来练习敲一遍右侧课件中的代码【身体质量指标BMI 3】")
m.代码消息(206, "", "身体质量指数BMI 3 ", "42.3.py",
       image="https://python123.io/images/f5/23/7a0eabbef50fc125c99da2e0e0bd.png",
       fill="manual",
       code_type="browser")

m.文本消息(207, "", "三套代码敲完了，只要你不偷懒，不用“帮我敲”一定能有熟练的“键盘感”")

# 42-03-身体质量指数BMI举一反三.mp4
m.检查点(30, "3.身体质量指数BMI举一反三")
m.视频消息(300, '', 'https://video.python123.io/sv/3ff3d3f1-175de054090/3ff3d3f1-175de054090.mp4')

m.生成消息文件(42)
