import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
img = np.array(Image.open('lighthouse2.jpg'))
grey = np.average(img, weights=(0.3,0.59,0.11), axis=2).astype(np.uint8)
grey = grey.reshape(grey.shape + (1,))
grey = np.repeat(grey, 3, axis=2)
minval = np.min(grey)
maxval = np.max(grey)
print(minval, maxval)
grey = (grey - minval) / (maxval - minval) * 255
plt.imshow(grey.astype(np.uint8))
plt.show()
