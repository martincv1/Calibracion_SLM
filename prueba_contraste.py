import numpy as np
import matplotlib.pyplot as plt
import cv2

imagen = cv2.imread('fotos_rot/3004_I30_0_T22_r.png')
plt.imshow(imagen)
plt.show()

index_find = imagen.argmax()
index = np.unravel_index(index_find, imagen.shape)
print(imagen[index])
for i in range(len(imagen[:,0,0])):
    for j in range(len(imagen[0,:,0])):
        imagen[i,j,0] = int(np.floor(imagen[i,j,0]*255/imagen[index]))

plt.imshow(imagen[:,:,0])
plt.show()
