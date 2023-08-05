import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
img = np.array(Image.open('lighthouse.jpg'))
img3 = img[:, ::-1, :]
plt.imshow(img3)
plt.show()
