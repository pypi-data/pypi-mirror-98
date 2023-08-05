import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
img = np.array(Image.open('lighthouse.jpg'))
img1 = np.rot90(img, 1, axes=(0,1))
plt.imshow(img1)
plt.show()
