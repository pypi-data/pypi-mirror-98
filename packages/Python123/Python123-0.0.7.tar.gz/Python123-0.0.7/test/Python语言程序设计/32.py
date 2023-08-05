from Python123 import MessageCommon

m = MessageCommon()

# 32-01-天天向上的力量问题分析.mp4
m.检查点(10, "1.天天向上的力量问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/40c5c01e-175de04ca72/40c5c01e-175de04ca72.mp4')

# 32-02-天天向上的力量第一问.mp4
m.检查点(20, "2.天天向上的力量第一问")
m.视频消息(200, '', 'https://video.python123.io/sv/4cdbf66-175de04cc54/4cdbf66-175de04cc54.mp4')

m.文本消息(201, "", "我们现在演练一下视频中，【天天向上力量 1】的 Python 数学实例")
m.代码消息(202, "", "天天向上的力量1", "32.1.py",
       image="https://python123.io/images/19/46/46b427be0205bd004b56e2d0e26c.png",
       fill="manual")

# 32-03-天天向上的力量第二问.mp4
m.检查点(30, "3.天天向上的力量第二问")
m.视频消息(300, '', 'https://video.python123.io/sv/1eed9098-175de04cf24/1eed9098-175de04cf24.mp4')
m.代码消息(301, "", "天天向上的力量2", "32.2.py",
       image="https://python123.io/images/4b/49/903be92ec485f535e5d5ddd15592.png",
       fill="manual")

# 32-04-天天向上的力量第三问.mp4
m.检查点(40, "4.天天向上的力量第三问")
m.视频消息(400, '', 'https://video.python123.io/sv/4a75f9fa-175de04d041/4a75f9fa-175de04d041.mp4')
m.代码消息(401, "", "天天向上的力量3", "32.3.py",
       image="https://python123.io/images/ac/e1/fe6973c87b957562508596f9f20a.png",
       fill="manual")

# 32-05-天天向上的力量第四问.mp4
m.检查点(50, "5.天天向上的力量第四问")
m.视频消息(500, '', 'https://video.python123.io/sv/4e033dbe-175de04d090/4e033dbe-175de04d090.mp4')
m.代码消息(501, "", "天天向上的力量4", "32.4.py",
       image="https://python123.io/images/db/eb/afedc864c73f002f8185292f958f.png",
       fill="manual")
m.文本消息(1091, "", "非常棒！你已经完成了 <b>天天向上系列</b> 的训练。给自己点个赞吧")

# 32-06-天天向上的力量举一反三.mp4
m.检查点(60, "6.天天向上的力量举一反三")
m.视频消息(600, '', 'https://video.python123.io/sv/441918b1-175de04d5b7/441918b1-175de04d5b7.mp4')
m.代码消息(601, "", "举一反三，你有更有创意的计算方法吗，快来试试？", "32.4.py")

m.生成消息文件(32)
