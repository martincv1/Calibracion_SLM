import numpy as np
import matplotlib.pyplot as plt
from skimage import draw
from scipy.signal import correlate2d
from skimage.registration import phase_cross_correlation


def simular_imagen(Nx=640, Ny=512, angulo_slm_max=1, slm_ancho=500, slm_alto=350, angulo_franjas_max=5,
                   fase1=0, fase2=np.pi, frecuencia=100, fotones_por_cuenta=5):
    """
    Simula una imagen con un SLM (Spatial Light Modulator) rotados aleatoriamente y con franjas de interferencia con
    fase distinta para las mitades superior e inferior.

    Parámetros:
    Nx (int): Ancho de la imagen en píxeles. Default es 640.
    Ny (int): Altura de la imagen en píxeles. Default es 512.
    angulo_max (float): Ángulo máximo de rotación en grados. Default es 4.
    slm_ancho (int): Ancho del SLM en píxeles. Default es 200.
    slm_alto (int): Altura del SLM en píxeles. Default es 200.
    angulo_franjas_max (float): Ángulo máximo de rotación de las franjas en grados. Default es 0.
    fase1 (float): Fase inicial para la primera mitad del SLM. Default es 0.
    fase2 (float): Fase inicial para la segunda mitad del SLM. Default es np.pi.
    frecuencia (float): Frecuencia espacial de las franjas en el SLM. Debe ser un valor positivo que represente el
                        número de ciclos que entra en un ancho de imagen.

    Retorna:
    numpy.ndarray: Imagen simulada como un array de 2D numpy de tipo uint8.

    Lanza:
    ValueError: Si el SLM rotado no entra dentro de la imagen.
    """

    theta = np.radians(np.random.uniform(-angulo_slm_max, angulo_slm_max))
    theta_franjas = np.radians(90 + np.random.uniform(-angulo_franjas_max, angulo_franjas_max))
    rotacion = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    x = np.arange(Nx)
    y = np.arange(Ny)
    xy = np.meshgrid(x, y)
    xy = np.dot(np.column_stack((xy[0].flatten(), xy[1].flatten())), rotacion)
    x_rot = xy[:, 0].reshape((Ny, Nx))
    y_rot = xy[:, 1].reshape((Ny, Nx))
    x_izquierda = Nx // 2 - slm_ancho // 2
    x_derecha = Nx // 2 + slm_ancho // 2
    slm1 = np.logical_and(x_rot > x_izquierda, x_rot < x_derecha)
    slm1 = np.logical_and(slm1, y_rot > Ny // 2)
    slm1 = np.logical_and(slm1, y_rot < Ny // 2 + slm_alto // 2)
    slm2 = np.logical_and(x_rot > x_izquierda, x_rot < x_derecha)
    slm2 = np.logical_and(slm2, y_rot > Ny // 2 - slm_alto // 2)
    slm2 = np.logical_and(slm2, y_rot <= Ny // 2)
    # Calcular los valores de x e y del rectangulo girado
    center = np.array([Nx // 2, Ny // 2])
    esquina_1 = np.dot(rotacion, np.array([-slm_ancho // 2, -slm_alto // 2]) + center)
    esquina_2 = np.dot(rotacion, np.array([slm_ancho // 2, -slm_alto // 2]) + center)
    esquina_3 = np.dot(rotacion, np.array([slm_ancho // 2, slm_alto // 2]) + center)
    esquina_4 = np.dot(rotacion, np.array([-slm_ancho // 2, slm_alto // 2]) + center)
    xmin = np.min([esquina_1[0], esquina_2[0], esquina_3[0], esquina_4[0]])
    xmax = np.max([esquina_1[0], esquina_2[0], esquina_3[0], esquina_4[0]])
    ymin = np.min([esquina_1[1], esquina_2[1], esquina_3[1], esquina_4[1]])
    ymax = np.max([esquina_1[1], esquina_2[1], esquina_3[1], esquina_4[1]])
    if not (0 <= xmin < Nx and 0 <= xmax < Nx and 0 <= ymin < Ny and 0 <= ymax < Ny):
        raise ValueError('El slm girado no entra en la imagen')
    imagen = np.zeros((Ny, Nx))
    imagen[slm1] = np.sin(2 * np.pi * frecuencia * (np.sin(theta_franjas) * x_rot[slm1] / Nx +
                                                    np.cos(theta_franjas) * y_rot[slm1] / Ny) + fase1) + 1
    imagen[slm2] = np.sin(2 * np.pi * frecuencia * (np.sin(theta_franjas) * x_rot[slm2] / Nx +
                                                    np.cos(theta_franjas) * y_rot[slm2] / Ny) + fase2) + 1
    imagen[slm1 | slm2] *= 120

    # Agregamos el contorno del SLM
    esquina_1 = np.round(esquina_1).astype(int)
    esquina_2 = np.round(esquina_2).astype(int)
    esquina_3 = np.round(esquina_3).astype(int)
    esquina_4 = np.round(esquina_4).astype(int)
    rr, cc = draw.polygon_perimeter([esquina_1[1], esquina_2[1], esquina_3[1], esquina_4[1]],
                                    [esquina_1[0], esquina_2[0], esquina_3[0], esquina_4[0]])
    imagen[rr, cc] = 255
    # Agregamos ruido de poisson
    imagen = np.random.poisson(imagen * fotones_por_cuenta) / fotones_por_cuenta
    imagen[imagen > 255] = 255
    imagen = imagen.astype(np.uint8)

    return imagen


imagen = simular_imagen(Nx=640, Ny=512, angulo_slm_max=1, slm_ancho=500, slm_alto=350, angulo_franjas_max=5,
                   fase1=0, fase2=np.pi, frecuencia=100, fotones_por_cuenta=5)
#print(imagen.shape)
#plt.imshow(imagen, cmap='gray')
#plt.show()

#Hago los recortes para la parte inferior y superior

alto, ancho = imagen.shape
#Defino alto y ancho de los rectangulos
h = 50
w = 100

#Doy el punto de referencia con int para que no falle después
x0_ref = int(ancho//1.6)
y0_ref = int(alto//1.5)

x1 = x0_ref
y1 = y0_ref - 200

# Coordenadas del rectángulo 1 (borde)
r_inicio = y1
r_fin = y1 + h
c_inicio = x1
c_fin = x1 + w

#Coordenadas del rect 2 (borde)
r2_inicio = y0_ref
r2_fin = y0_ref + h
c2_inicio = x0_ref
c2_fin = x0_ref + w

# Dibujar el rectángulo (solo el borde) en blanco (valor 255)
imagen_marcada = imagen.copy()
rr, cc = draw.rectangle_perimeter(start=(r_inicio, c_inicio), end=(r_fin , c_fin), shape=imagen.shape)
rrr, ccc = draw.rectangle_perimeter(start=(r2_inicio, c2_inicio), end=(r2_fin, c2_fin), shape=imagen.shape)
imagen_marcada[rr, cc] = 255
imagen_marcada[rrr, ccc] = 255

# Ploteo la imagen con los dos rectangulos marcados
plt.imshow(imagen_marcada, cmap='gray')
plt.axis()
plt.show()

# Defino regiones para correlación

region_inf = imagen[r_inicio:r_fin, c_inicio:c_fin]
region_sup = imagen[r2_inicio:r2_fin, c2_inicio:c2_fin]

# Crear figura para visualizar ambas regiones 
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Mostrar región inferior
axs[0].imshow(region_inf, cmap='gray')
axs[0].set_title("Región inferior")
axs[0].axis('off')

# Mostrar región superior
axs[1].imshow(region_sup, cmap='gray')
axs[1].set_title("Región superior")
axs[1].axis('off')

plt.tight_layout()
plt.show()


# Calcular la correlación cruzada 2D
correlacion = correlate2d(region_inf.astype(np.float32), region_sup.astype(np.float32), mode='full')

# Mostrar la correlación
plt.imshow(correlacion, cmap='viridis')
plt.colorbar(label='Correlación')
plt.title("Correlación cruzada 2D")
plt.axis('off')
plt.show()
# Calcular la correlación cruzada con skimage
correlacion_2 = phase_cross_correlation(region_inf.astype(np.float32), region_sup.astype(np.float32), upsample_factor= 1)

print(correlacion_2[0])  #se supone que pasa los shifts, no lo entiendo bien la verdad