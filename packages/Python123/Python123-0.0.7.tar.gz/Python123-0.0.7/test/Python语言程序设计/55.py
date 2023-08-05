from Python123 import MessageCommon

m = MessageCommon()

# 55-01-科赫雪花小包裹问题分析.mp4
m.检查点(10, "1.科赫雪花小包裹问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/5dd98244-175de05c3db/5dd98244-175de05c3db.mp4')

# 55-02-科赫雪花小包裹实例讲解(上).mp4
m.检查点(20, "2.科赫雪花小包裹实例讲解(上)")
m.视频消息(200, '', 'https://video.python123.io/sv/16d9c3c6-175de05c68a/16d9c3c6-175de05c68a.mp4')

# 55-03-科赫雪花小包裹实例讲解(下).mp4
m.检查点(30, "3.科赫雪花小包裹实例讲解(下)")
m.视频消息(300, '', 'https://video.python123.io/sv/2a77894e-175de05c97a/2a77894e-175de05c97a.mp4')

m.文本消息(107, "", "下面是采用递归方法绘制科赫曲线的实例，分形几何采用类似递归的核心思想")
m.代码消息(108, "", "科赫曲线 1", "55.1.py",
       image="https://python123.io/images/b2/2b/ec22342368d0c05e02899ac978ec.png",
       fill="manual",
       code_type="browser")

m.代码消息(109, "", "科赫曲线 2", "55.2.py",
       image="https://python123.io/images/38/26/5782d5f72d8d6ea06a4ddfb0f07d.png",
       fill="manual",
       code_type="browser")

# 55-04-科赫雪花小包裹举一反三.mp4
m.检查点(40, "4.科赫雪花小包裹举一反三")
m.视频消息(400, '', 'https://video.python123.io/sv/34b9f4ec-175de05cd4f/34b9f4ec-175de05cd4f.mp4')

m.生成消息文件(55)
