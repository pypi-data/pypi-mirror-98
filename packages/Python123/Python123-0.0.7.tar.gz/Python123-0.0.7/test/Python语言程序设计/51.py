from Python123 import MessageCommon

m = MessageCommon()

# 51-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/4e6533fa-175de057911/4e6533fa-175de057911.mp4')

# 51-02-函数的理解和定义.mp4
m.检查点(20, "2.函数的理解和定义")
m.视频消息(200, '', 'https://video.python123.io/sv/45b78229-175de057aa6/45b78229-175de057aa6.mp4')

# 51-03-函数的使用及调用过程.mp4
m.检查点(30, "3.函数的使用及调用过程")
m.视频消息(300, '', 'https://video.python123.io/sv/1196edf5-175de057c76/1196edf5-175de057c76.mp4')
m.代码消息(301, "", "函数的使用及调用过程", "51.1.py", code_type="browser")

# 51-04-函数的参数传递.mp4
m.检查点(40, "4.函数的参数传递")
m.视频消息(400, '', 'https://video.python123.io/sv/55e9f56b-175de0580c7/55e9f56b-175de0580c7.mp4')
m.代码消息(401, "", "函数的可变参数传递", "51.2.py", code_type="browser")

# 51-05-函数的返回值.mp4
m.检查点(50, "5.函数的返回值")
m.视频消息(500, '', 'https://video.python123.io/sv/2c5880eb-175de05828f/2c5880eb-175de05828f.mp4')

# 51-06-局部变量和全局变量.mp4
m.检查点(60, "6.局部变量和全局变量")
m.视频消息(600, '', 'https://video.python123.io/sv/1ca813c2-175de05857f/1ca813c2-175de05857f.mp4')
m.代码消息(601, "", "局部变量和全局变量 - 1", "51.3.py", code_type="browser")
m.代码消息(602, "", "局部变量和全局变量 - 2", "51.4.py", code_type="browser")

# 51-07-lambda函数.mp4
m.检查点(70, "7.lambda函数")
m.视频消息(700, '', 'https://video.python123.io/sv/17142d8b-175de05890b/17142d8b-175de05890b.mp4')
m.代码消息(701, "", "lambda函数", "51.5.py")

# 51-08-单元小结.mp4
m.检查点(80, "8.单元小结")
m.视频消息(800, '', 'https://video.python123.io/sv/44c2ce75-175de058948/44c2ce75-175de058948.mp4')

m.生成消息文件(51)
