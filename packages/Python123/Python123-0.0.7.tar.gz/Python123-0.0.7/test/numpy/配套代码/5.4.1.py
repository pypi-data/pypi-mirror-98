import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
img = np.array(Image.open('lighthouse.jpg'))

for i in range(50):
    h = np.random.randint(10, 100)
    w = np.random.randint(10, 100)
    x = np.random.randint(0, img.shape[1] - w)
    y = np.random.randint(0, img.shape[0] - h)
    if i % 2 == 0:
        img[y:y+h, x:x+w, :1] = 255
    else:
        img[y:y+h, x:x+w, 1:2] = 200
img = Image.fromarray(img)
plt.imshow(img)
plt.show()
