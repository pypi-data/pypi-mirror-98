from Python123 import MessageCommon

m = MessageCommon()

# 81-01-体育竞技分析问题分析.mp4
m.检查点(10, "1.体育竞技分析问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/c7eb0b3-175de069db9/c7eb0b3-175de069db9.mp4')

# 81-02-自顶向下和自底向上.mp4
m.检查点(20, "2.自顶向下和自底向上")
m.视频消息(200, '', 'https://video.python123.io/sv/3097d59e-175de069e01/3097d59e-175de069e01.mp4')

# 81-03-体育竞技分析实例解析.mp4
m.检查点(30, "3.体育竞技分析实例解析")
m.视频消息(300, '', 'https://video.python123.io/sv/59ddbc32-175de06a0d9/59ddbc32-175de06a0d9.mp4')

# 实例 体育竞技分析
m.检查点(40, "4.体育竞技分析")
m.代码消息(301, "", "体育竞技分析", "81.1.py",
       image="https://python123.io/images/a3/cd/d257a9db96b90ff2449b02b3bbba.png",
       fill="manual",
       code_type="browser")

# 81-04-体育竞技分析举一反三.mp4
m.检查点(50, "5.体育竞技分析举一反三")
m.视频消息(400, '', 'https://video.python123.io/sv/5844213f-175de06a419/5844213f-175de06a419.mp4')

m.生成消息文件(81)
