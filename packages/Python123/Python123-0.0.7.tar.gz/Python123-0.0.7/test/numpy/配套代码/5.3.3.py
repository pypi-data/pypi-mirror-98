import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

img = np.array(Image.open('lighthouse.jpg'))
img = img.astype(np.uint16)
img[:, :, 0] += 100
img = img.clip(0, 255)
plt.imshow(img.astype(np.uint8))
plt.show()
