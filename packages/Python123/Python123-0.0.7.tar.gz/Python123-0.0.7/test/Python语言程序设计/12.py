from Python123 import MessageCommon

m = MessageCommon()

# 12-01-单元开篇.mp4
m.检查点(10, "1.单元开篇")
m.视频消息(100, '', 'https://video.python123.io/sv/8852340-175de041616/8852340-175de041616.mp4')

# 12-02-Python语言概述.mp4
m.检查点(20, "2.Python语言概述")
m.视频消息(200, '', 'https://video.python123.io/sv/2f677edc-175de04161f/2f677edc-175de04161f.mp4')

# 12-03-Python语言Windows系统开发环境.mp4
m.检查点(30, "3.Python语言Windows系统开发环境")
m.视频消息(300, '', 'https://video.python123.io/sv/500b0ddf-175de0416f8/500b0ddf-175de0416f8.mp4')
m.文本消息(301, "", "安装过程中一定要勾选，add python 3.xx to PATH 选择框，不然在后面的学习过程中会需要你手动添加环境变量")
m.文本消息(302, "", "本节是安装视频，所以没有声音，对于更多的操作系统Mac、Linux因版本不同需要自行查询相关的安装教程")
m.文本消息(303, "", "最开始学习的使用推荐大家使用IDLE，熟练掌握后可以使用Pycharm、vscode、anaconda等集成开发环境")
m.文本消息(304, "", "集成开发环境提供自动保存、高亮显示、智能代码补全、实时错误检查和快速修复功能等功能")
# 12-04-Python程序编写与运行.mp4
m.检查点(40, "4.Python程序编写与运行")
m.视频消息(400, '', 'https://video.python123.io/sv/201039a5-175de041757/201039a5-175de041757.mp4')

# 12-05-单元小结.mp4
m.检查点(50, "5.单元小结")
m.视频消息(500, '', 'https://video.python123.io/sv/33cf205e-175de0419f3/33cf205e-175de0419f3.mp4')

m.生成消息文件(12)
