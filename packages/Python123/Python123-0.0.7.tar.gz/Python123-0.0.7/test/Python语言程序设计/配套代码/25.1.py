# 正方形填充
import turtle as t

t.colormode(255)
t.fillcolor(255, 200, 208)  # 设置填充颜色
t.begin_fill()  # 开始填充
for i in range(4):
    t.fd(100)
    t.left(90)
t.end_fill()  # 结束填充
