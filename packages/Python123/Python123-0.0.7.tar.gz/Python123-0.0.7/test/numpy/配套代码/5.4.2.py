import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math

img = np.array(Image.open('lighthouse.jpg'))
bs = block_size = 50
for i in range(math.ceil(img.shape[0] / bs)):
    for j in range(math.ceil(img.shape[1] / bs)):
        s = [slice(i*bs,(i+1)*bs), slice(j*bs,(j+1)*bs)]
        img[s] = np.median(img[s], axis=(0,1))
plt.imshow(img.astype('uint8'))
img = Image.fromarray(img)
plt.imshow(img)
plt.show()
