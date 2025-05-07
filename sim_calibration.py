import numpy as np
import matplotlib.pyplot as plt
from skimage import draw
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks

import interfranja as ifranja


MINIMUM_DISTANCE_PEAKS = 10
PROMINENCE_PEAKS = 1
SHOW_CROP1 = False
SHOW_INTERFRANJA = False


def simular_imagen(Nx=640, Ny=512, angulo_slm_max=1, slm_ancho=500, slm_alto=350, angulo_franjas_max=5,
                   fase1=0, fase2=np.pi, frecuencia=10, fotones_por_cuenta=5, amplitud_imperfecciones=0.25):
    """
    Simula una imagen con un SLM (Spatial Light Modulator) rotados aleatoriamente y con franjas de interferencia con
    fase distinta para las mitades superior e inferior.

    Parámetros:
    Nx (int): Ancho de la imagen en píxeles. Default es 640.
    Ny (int): Altura de la imagen en píxeles. Default es 512.
    angulo_slm_max (float): Ángulo máximo de rotación del SLM en grados. Default es 1.
    slm_ancho (int): Ancho del SLM en píxeles. Default es 500.
    slm_alto (int): Altura del SLM en píxeles. Default es 350.
    angulo_franjas_max (float): Ángulo máximo de rotación de las franjas en grados. Default es 5.
    fase1 (float): Fase inicial para la primera mitad del SLM. Default es 0.
    fase2 (float): Fase inicial para la segunda mitad del SLM. Default es pi.
    frecuencia (float): Frecuencia espacial de las franjas en el SLM. Debe ser un valor positivo que represente el
                        número de ciclos que entra en un ancho de imagen. Default es 10.
    fotones_por_cuenta (int): Número de fotones que se generan por cada punto del SLM. Default es 5.
    amplitud_imperfecciones (float): Amplitud de las imperfecciones aleatorias en la imagen. Default es 0.25.

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
    # Calcular fase de superficie imperfecta
    fase_imperfecta = gaussian_filter(np.random.randn(Ny, Nx), sigma=100, mode='reflect')
    fase_imperfecta = fase_imperfecta / np.max(fase_imperfecta) * amplitud_imperfecciones * 2 * np.pi

    # Generar la imagen
    imagen = np.zeros((Ny, Nx))
    imagen[slm1] = np.sin(2 * np.pi * frecuencia * (np.sin(theta_franjas) * x_rot[slm1] / Nx +
                                                    np.cos(theta_franjas) * y_rot[slm1] / Ny)
                          + fase1 + fase_imperfecta[slm1]) + 1
    imagen[slm2] = np.sin(2 * np.pi * frecuencia * (np.sin(theta_franjas) * x_rot[slm2] / Nx +
                                                    np.cos(theta_franjas) * y_rot[slm2] / Ny)
                          + fase2 + fase_imperfecta[slm2]) + 1
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


def get_shift_cross_correlation(imagen1, imagen2, padding=0):
    if padding > 0:
        imagen1 = np.pad(imagen1, padding)
        imagen2 = np.pad(imagen2, padding)
    cross_corr = np.real(np.fft.ifft2(np.fft.fft2(imagen1) * np.conj(np.fft.fft2(imagen2))))
    cross_corr = np.fft.fftshift(cross_corr)
    indices = np.unravel_index(np.argmax(cross_corr), cross_corr.shape)
    shift = indices[0] - cross_corr.shape[0] // 2, indices[1] - cross_corr.shape[1] // 2
    return shift


def get_dphi_fft1d(imagen1, imagen2, get_shift=False):
    signal1 = np.sum(imagen1, axis=0)
    signal2 = np.sum(imagen2, axis=0)
    f_signal1 = np.fft.fft(signal1 - np.mean(signal1))
    f_signal2 = np.fft.fft(signal2 - np.mean(signal2))
    freq1 = np.argmax(np.abs(f_signal1))
    freq2 = np.argmax(np.abs(f_signal2))
    if freq1 != freq2:
        raise ValueError("Las franjas no tienen la misma frecuencia espacial")
    dfase = np.angle(f_signal1[freq1] / f_signal2[freq2])

    if get_shift:
        N1 = len(signal1)
        shift = dfase / (2 * np.pi * freq1) * N1
        return shift
    return dfase


def get_interfranja(imagen, remove_Gaussian_profile=False, show=False):
    # Rotar la imagen para dejar las franjas más o menos verticales
    img_rotada = ifranja.rotate_image_to_max_frequency(imagen)

    intensity_profile = np.mean(img_rotada, axis=0)
    if remove_Gaussian_profile:
        intensity_profile = ifranja.remove_gaussian_from_curve(intensity_profile)

    if show:
        # Mostrar la imagen original y la rotada
        fig, axs = plt.subplots(1, 3, figsize=(8, 8))
        axs[0].title.set_text("Imagen Original")
        axs[0].imshow(imagen, cmap='gray')
        axs[1].title.set_text("Imagen Rotada")
        im = axs[1].imshow(img_rotada, cmap='gray')
        fig.colorbar(im, ax=axs[1])
        axs[2].plot(intensity_profile)
        plt.show()
    # Encontrar los mínimos en el perfil de intensidad
    peaks, _ = find_peaks(-intensity_profile, distance=MINIMUM_DISTANCE_PEAKS,
                          prominence=PROMINENCE_PEAKS)
    return np.mean(np.diff(peaks))


imagen = simular_imagen(frecuencia=25)
crop = imagen[90:220, 100:550]
if SHOW_CROP1:
    fig, axs = plt.subplots(1, 2, figsize=(8, 8))
    axs[0].imshow(imagen, cmap='gray')
    axs[1].imshow(crop, cmap='gray')
    plt.show()

if SHOW_INTERFRANJA:
    interfranja = get_interfranja(crop, remove_Gaussian_profile=False, show=True)
    print(f"Diferencia entre picos promedio: {interfranja}")

# Análisis de correlación cruzada
# crop2 = imagen[270:400, 100:550]
r_shift = 0
c_shift = 12
crop2 = imagen[90+r_shift:220+r_shift, 100+c_shift:550+c_shift]

shift = get_dphi_fft1d(crop2, crop, get_shift=True)
print(f"Shift: {shift}")
