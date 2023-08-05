from random import random
import turtle as t

t.setup(1000, 600)
t.tracer(100)
t.bgcolor("black")

DARTS = 100 * 100
hits = 0.0
for i in range(1, DARTS + 1):
    x, y = random(), random()
    dist = pow(x ** 2 + y ** 2, 0.5)
    if dist <= 1.0:
        hits += 1
        t.penup()
        t.pencolor("blue")
        t.goto(x * 200, y * 200)
        t.dot(2)
        t.pendown()
    else:
        t.penup()
        t.pencolor("white")
        t.goto(x * 200, y * 200)
        t.dot(2)
        t.pendown()
pi = 4 * (hits / DARTS)
print(pi)
t.done()
