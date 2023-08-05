import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
img = np.array(Image.open('lighthouse.jpg'))
img2 = np.rot90(img, 3, axes=(0,1))
plt.imshow(img2)
plt.show()
