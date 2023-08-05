import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = np.array(Image.open('lighthouse.jpg'))
img4 = np.roll(img.copy(), -100, axis=0)
img4[-100:, :, :] = 255
plt.imshow(img4)
plt.show()
