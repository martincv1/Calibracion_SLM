import numpy as np
import matplotlib.pyplot as plt
import cv2

imagen = cv2.imread('fotos_rot/3004_I230_0_T22_r.png')
plt.imshow(imagen)
plt.show()

index_find = imagen.argmax()
index = np.unravel_index(index_find, imagen.shape)
print(imagen[index])
imagen *= 255//37

plt.imshow(imagen)
plt.show()
