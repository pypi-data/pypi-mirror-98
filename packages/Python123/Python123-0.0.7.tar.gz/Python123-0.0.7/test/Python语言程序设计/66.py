from Python123 import MessageCommon

m = MessageCommon()

# 66-01-文本词频统计问题分析.mp4
m.检查点(10, "1.文本词频统计问题分析")
m.视频消息(100, '', 'https://video.python123.io/sv/3e16918b-175de062777/3e16918b-175de062777.mp4')

# 66-02-Hamlet英文词频统计实例讲解.mp4
m.检查点(20, "2.Hamlet英文词频统计实例讲解")
m.视频消息(200, '', 'https://video.python123.io/sv/57f3dffc-175de062878/57f3dffc-175de062878.mp4')

# 实例 哈姆雷特英文词频统计
m.检查点(30, "3.哈姆雷特英文词频统计")
m.文本消息(201, "", "哈姆雷特英文词频统计")
m.代码消息附件(202, "", "哈姆雷特英文词频统计", "66.1.py",
         image="https://python123.io/images/6c/d1/45f948521b89e91b676b994933db.png",
         fill="manual",
         attachements_name="hamlet.txt")

# 66-03-《三国演义》人物出场统计实例讲解(上).mp4
m.检查点(40, "4.《三国演义》人物出场统计实例讲解(上)")
m.视频消息(300, '', 'https://video.python123.io/sv/3c000d2a-175de0629c9/3c000d2a-175de0629c9.mp4')

# 66-04-《三国演义》人物出场统计实例讲解(下).mp4
m.检查点(50, "5.《三国演义》人物出场统计实例讲解(下)")
m.视频消息(400, '', 'https://video.python123.io/sv/2f73feff-175de062a1f/2f73feff-175de062a1f.mp4')

# 实例 三国演义人物出场统计
m.检查点(60, "6.三国演义人物出场统计")
m.代码消息附件(401, "", "三国演义人物出场统计 1 ", "66.2.py",
         image="https://python123.io/images/e7/1d/5e1d20fd53f0d0cd22b537ee1867.png",
         fill="manual",
         attachements_name="threekingdoms.txt")
m.代码消息附件(402, "", "三国演义人物出场统计 2 ", "66.3.py",
         image="https://python123.io/images/2d/9c/8502997d30a1795cdf43aa58bc82.png",
         fill="manual",
         attachements_name="threekingdoms.txt")

# 66-05-文本词频统计举一反三.mp4
m.检查点(70, "7.文本词频统计举一反三")
m.视频消息(500, '', 'https://video.python123.io/sv/4b48ae32-175de063309/4b48ae32-175de063309.mp4')

m.生成消息文件(66)
