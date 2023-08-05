import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = np.array(Image.open('lighthouse.jpg'))
plt.imshow(img)
plt.show()
print(img.shape, img.dtype)
