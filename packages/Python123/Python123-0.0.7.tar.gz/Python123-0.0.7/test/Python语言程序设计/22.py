from Python123 import MessageCommon

m = MessageCommon()

# 22-01-Python蟒蛇绘制问题分析.mp4
m.检查点(10, "1.Python蟒蛇绘制问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/1be6b4c9-175de046ebb/1be6b4c9-175de046ebb.mp4')

# 22-02-Python蟒蛇绘制实例编写.mp4
m.检查点(20, "2.Python蟒蛇绘制实例编写")
m.视频消息(200, '', 'https://video.python123.io/sv/4211c309-175de0471c7/4211c309-175de0471c7.mp4')

# 实例2 Python蟒蛇的绘制
m.检查点(30, "3.Python蟒蛇的绘制")
m.文本消息(105, "", "结合 Python 蟒蛇绘制案例，分析 turtle 库语法元素，包括绘图坐标体系、画笔控制函数和形状绘制函数等")
m.文本消息(1051, "", "下图，左侧是给你的代码窗口，右侧是课程中的 PPT 内容，请按照右侧的内容，敲一遍代码，一起演练一遍吧。")
m.代码消息(106, "", "对照敲出", "22.1.py",
       image="https://python123.io/images/05/a6/1d81f057aecfd23fdd6e6e734abb.png",
       fill="manual",
       code_type="browser")

m.文本消息(107, "", "如果你已经掌握蟒蛇的绘制，那么不妨看看 Python123 的海龟绘图专区，拥有大量的优质 turtle 绘图作品")
m.文本消息(1071, "", "下面链接可以看到所有同学们的作品，也希望能看到你的作品")
m.图片消息(108, "", "https://python123.io/images/9d/6c/444d290510ea8198d8876d990e0d.png")

# 22-03-Python蟒蛇绘制举一反三.mp4
m.检查点(40, "4.Python蟒蛇绘制举一反三")
m.视频消息(300, '', 'https://video.python123.io/sv/2f4243ef-175de047a7c/2f4243ef-175de047a7c.mp4')

m.文本消息(301, "", "举一反三，尝试改变蟒蛇的颜色、长度和方向吧！")

m.代码消息(302, "", "下面是示例蟒蛇的代码，试着举一反三吧！", "22.1.py", code_type="browser")

m.生成消息文件(22)
