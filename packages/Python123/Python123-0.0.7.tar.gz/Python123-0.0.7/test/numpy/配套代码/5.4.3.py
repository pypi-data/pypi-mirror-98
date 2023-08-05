import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = np.array(Image.open('lighthouse.jpg'))
h, w = img.shape[:2]
m = np.linspace(1, 0, h).reshape(h, 1, 1)
img = img * m
plt.imshow(img.astype('uint8'))
plt.show()
