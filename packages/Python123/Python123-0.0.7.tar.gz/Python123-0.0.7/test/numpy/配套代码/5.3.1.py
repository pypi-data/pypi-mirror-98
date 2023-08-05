import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

img = np.array(Image.open('lighthouse2.jpg'))

grey = np.average(img, weights=(0.3, 0.59, 0.11), axis=2).astype(np.uint8)
print(grey.shape)
grey = grey[:, :, np.newaxis]
grey = np.repeat(grey, 3, axis=2)
plt.imshow(grey)
plt.show()
