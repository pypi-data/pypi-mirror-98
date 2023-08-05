from Python123 import MessageCommon

m = MessageCommon()

# 53-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/4e5c829c-175de059ddb/4e5c829c-175de059ddb.mp4')

# 53-02-代码复用与模块化设计.mp4
m.检查点(20, "2.代码复用与模块化设计")
m.视频消息(200, '', 'https://video.python123.io/sv/2ee77373-175de059e0d/2ee77373-175de059e0d.mp4')

# 53-03-函数递归的理解.mp4
m.检查点(30, "3.函数递归的理解")
m.视频消息(300, '', 'https://video.python123.io/sv/31df1aeb-175de05ad56/31df1aeb-175de05ad56.mp4')
m.代码消息(301, "", "递归的实现", "53.1.py", code_type="browser")

# 53-04-函数递归的调用过程.mp4
m.检查点(40, "4.函数递归的调用过程")
m.视频消息(400, '', 'https://video.python123.io/sv/251ecca5-175de05afda/251ecca5-175de05afda.mp4')

# 53-05-函数递归实例解析.mp4
m.检查点(50, "5.函数递归实例解析")
m.视频消息(500, '', 'https://video.python123.io/sv/c70f488-175de05b3c8/c70f488-175de05b3c8.mp4')
m.代码消息(501, "", "字符串反转", "53.2.py", code_type="browser")
m.代码消息(502, "", "斐波那契数列", "53.3.py", code_type="browser")
m.代码消息(503, "", "汉诺塔", "53.4.py", code_type="browser")

# 53-06-单元小结.mp4
m.检查点(60, "6.单元小结")
m.视频消息(600, '', 'https://video.python123.io/sv/17886f0d-175de05b3ec/17886f0d-175de05b3ec.mp4')

m.生成消息文件(53)
