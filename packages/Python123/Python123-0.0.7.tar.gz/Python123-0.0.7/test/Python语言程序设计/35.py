from Python123 import MessageCommon

m = MessageCommon()

# 35-01-文本进度条问题分析.mp4
m.检查点(10, "1.文本进度条问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/5ccf2508-175de050e3c/5ccf2508-175de050e3c.mp4')

# 35-02-文本进度条简单的开始.mp4
m.检查点(20, "2.文本进度条简单的开始")
m.视频消息(200, '', 'https://video.python123.io/sv/1730f9ca-175de050f5d/1730f9ca-175de050f5d.mp4')

m.文本消息(201, "", "下面我们来做【文本进度条 1】练习")
# 文本进度条 1 2 3
m.代码消息(202, "", "文本进度条1", "35.1.py",
       image="https://python123.io/images/2d/e3/7acd2a6d180f000e2a56564ab0ec.png",
       fill="manual",
       code_type="browser")

# 35-03-文本进度条单行动态刷新.mp4
m.检查点(30, "3.文本进度条单行动态刷新")
m.视频消息(300, '', 'https://video.python123.io/sv/1a79f6e2-175de051669/1a79f6e2-175de051669.mp4')
m.文本消息(301, "", "我们继续【文本进度条 2】训练，再接再厉")
m.代码消息(302, "", "文本进度条2", "35.2.py",
       image="https://python123.io/images/8d/4e/c02a3bd0df8b88fa5030d850e179.png",
       fill="manual",
       code_type="browser")

# 35-04-文本进度条实例完整效果.mp4
m.检查点(40, "4.文本进度条实例完整效果")
m.视频消息(400, '', 'https://video.python123.io/sv/550c64d0-175de051696/550c64d0-175de051696.mp4')
m.文本消息(401, "", "下面我们来继续做【文本进度条 3】的训练")
m.代码消息(402, "", "文本进度条3，因为在线编辑器不能获得 CPU 时间，所以我们用 time 替代了 perf_counter 方法，也能实现同样的效果。", "35.3.py", code_type="browser")
m.文本消息(403, "", "【文本进度条 3】的训练，到这里就结束了，你感觉怎么样？可以发个表情告诉大家")

# 35-05-文本进度条举一反三.mp4
m.检查点(50, "5.文本进度条举一反三")
m.视频消息(500, '', 'https://video.python123.io/sv/5a2550dd-175de051b02/5a2550dd-175de051b02.mp4')

m.生成消息文件(35)
