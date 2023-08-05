# GovRptWordCloudv1.py
import jieba
import wordcloud

f = open("新时代中国特色社会主义.txt", "r", encoding="utf-8")

t = f.read()
f.close()
ls = jieba.lcut(t)

txt = " ".join(ls)
w = wordcloud.WordCloud(width=800, height=600, background_color="white", font_path="msyh.ttc")
w.generate(txt)
w.to_file("grwordcloud.png")
