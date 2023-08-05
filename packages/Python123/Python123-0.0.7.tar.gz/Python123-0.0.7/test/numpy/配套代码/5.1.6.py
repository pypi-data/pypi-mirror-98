import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = np.array(Image.open('lighthouse.jpg'))
img6 = img[150:600, 150:320,:]
plt.imshow(img6)
plt.show()
