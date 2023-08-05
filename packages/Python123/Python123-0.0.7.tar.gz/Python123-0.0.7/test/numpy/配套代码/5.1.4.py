import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = np.array(Image.open('lighthouse.jpg'))
height, width, _ = img.shape
img4 = img[:height // 2, :, :]
plt.imshow(img4)
plt.show()
