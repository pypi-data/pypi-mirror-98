from Python123 import MessageCommon

m = MessageCommon()
# 90-01-前课复习.mp4
m.检查点(10, "1.前课复习")
m.文本消息(98, "", "亲爱的【{name}】，您好，欢迎进入Python语言程序设计【第 9 周】互动课程")
m.文本消息(99, "", "本周主要面向科学计算和可视化，讲解多维数据运算第三方库 numpy 和科学计算可视化库 matplotlib，重点讲解绘制坐标系和雷达图的方法")


m.视频消息(100, '', 'https://video.python123.io/sv/240e94fc-175de06eaa2/240e94fc-175de06eaa2.mp4')

# 90-02-本课概要.mp4
m.检查点(20, "2.本课概要")
m.视频消息(200, '', 'https://video.python123.io/sv/11bd7258-175de06ead7/11bd7258-175de06ead7.mp4')

m.生成消息文件(90)
