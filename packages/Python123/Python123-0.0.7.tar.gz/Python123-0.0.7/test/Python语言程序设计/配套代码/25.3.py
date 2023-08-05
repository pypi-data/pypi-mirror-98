# turtle绘图速度
import turtle as t
t.setup(800,800)
t.tracer(100)
t.pensize(1)
for i in range(200):
    t.fd(1 * i)
    t.left(20)
t.right(175)
t.done()
