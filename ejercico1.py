import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread("Imagen_con_detalles_escondidos.tif", cv2.IMREAD_GRAYSCALE)

plt.imshow(img, cmap="gray")
plt.show()

def equalizacion_local(img, tamaño_ventana, truncate=False):

  m, n = tamaño_ventana
  borde = max(m, n)
  borde = borde//2

  resultado = img.copy()
  rows, col = resultado.shape

  if truncate:
     resultado[resultado > 200] = 255
     resultado[(resultado > 0) & (resultado < 15)] = 8

  img_bordes = cv2.copyMakeBorder(resultado, borde, borde, borde, borde, cv2.BORDER_REFLECT)

  for fila in range(rows):
    for columna in range(col):

        ventana = img_bordes[fila : fila + m, columna : columna + n]
        ventana_eq = cv2.equalizeHist(ventana)
        resultado[fila, columna] = ventana_eq[m//2, n//2]
  
  return resultado

k = 33

img_eq_3 = equalizacion_local(img, (k,k))
img_eq_3_truncate = equalizacion_local(img, (k,k), truncate=True)

plt.subplots(1,2,sharex=True, sharey=True)
plt.subplot(121)
plt.imshow(img_eq_3, cmap='gray')
plt.title('Img sin truncate')
plt.subplot(122)
plt.imshow(img_eq_3_truncate, cmap='gray')
plt.title('Img con truncate')
plt.show()

img_3 = equalizacion_local(img, (3,3))
img_15 = equalizacion_local(img, (15,15))
img_51 = equalizacion_local(img, (51,51))

plt.subplots(1,3,sharex=True, sharey=True)
plt.subplot(131)
plt.imshow(img_3, cmap='gray')
plt.title('Img sin truncate')
plt.subplot(132)
plt.imshow(img_15, cmap='gray')
plt.title('Img con truncate')
plt.subplot(133)
plt.imshow(img_51, cmap='gray')
plt.title('Img con truncate')
plt.show()

