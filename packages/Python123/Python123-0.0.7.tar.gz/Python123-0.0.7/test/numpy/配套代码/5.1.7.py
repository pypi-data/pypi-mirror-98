import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = np.array(Image.open('lighthouse.jpg'))
img7 = np.copy(img)
height, width, _ = img.shape
img7[:30, :, :] = 0
img7[height-30:, :, :] = 0

plt.imshow(img7)
plt.show()
