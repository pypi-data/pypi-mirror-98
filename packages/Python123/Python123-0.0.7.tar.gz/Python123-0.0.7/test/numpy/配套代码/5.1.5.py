import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = np.array(Image.open('lighthouse.jpg'))
height, width, _ = img.shape
img5 = img[:, width//3:, :]
plt.imshow(img5)
plt.show()
