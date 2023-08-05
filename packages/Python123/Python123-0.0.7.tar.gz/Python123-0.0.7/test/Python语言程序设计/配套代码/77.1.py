import jieba
import wordcloud
# from scipy.misc import imread
import numpy as np
from PIL import Image

mask = np.array(Image.open("fivestar.png"))
excludes = {}
f = open("新时代中国特色社会主义.txt", "r", encoding="utf-8")
t = f.read()
f.close()
ls = jieba.lcut(t)
txt = " ".join(ls)
w = wordcloud.WordCloud(
    width=800, height=600,
    background_color="white",
    font_path="msyh.ttc", mask=mask
)
w.generate(txt)
w.to_file("grwordcloudm.png")
