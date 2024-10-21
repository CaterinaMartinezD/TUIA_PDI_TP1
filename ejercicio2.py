import cv2
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------Lineas---------------------------------------------------------
def DetectarLineas(img, plot=False):

    # Sumamos los pixeles de cada fila y columna
    box_rows = np.sum(img, axis=1)
    box_cols = np.sum(img, axis=0)

    # Dividimos los valores para que esten en un rango mas acotado
    box_cols = box_cols // 255 
    box_rows = box_rows // 255

    # Las filas y columnas que sean menores a ese umbral son las de interes
    box_rows = [x for x in range(len(box_rows)) if box_rows[x] <= 260]
    box_cols = [x for x in range(len(box_cols)) if box_cols[x] <= 280]

    # La primer fila siempre van a ser los datos del estudiante
    datos_row = box_rows.pop(0)

    # Ploteo de las lineas detectadas (Opcional)
    if plot:

        plt.imshow(img, cmap='gray')

        cont_h = 0
        for idx, val in enumerate(box_rows):
            plt.axhline(y=val, color='red', linewidth=1)
            cont_h += 1

        cont_v = 0
        for idx, val in enumerate(box_cols):
            plt.axvline(x=idx, color='red', linewidth=1)
            cont_v += 1

        plt.title(f'Cantidad de lineas horizontales: {cont_h}, cantidad de lineas verticales: {cont_v}')
        plt.show()
    
    return box_rows, box_cols, datos_row

# ---------------------------------------Preguntas------------------------------------------------------
def DetectarPreguntas(img, box_rows, box_cols, plot=False):

    preguntas_ord = []
    preguntas = []

    # Para obtener las preguntas queremos:
    # - Todas las filas menos la ultima
    # - Los dos pares de columnas que hay.
    
    # Este bucle recorre las filas y columnas que nos interesan
    for i in range(len(box_rows) - 1):
        for j in range(0, len(box_cols), 2):

            # Obtenemos la pregunta
            r_inicio = box_rows[i]
            r_final = box_rows[i + 1]
            c_inicio = box_cols[j]
            c_final = box_cols[j + 1]

            # Y la agregamos
            preguntas.append(img[r_inicio:r_final, c_inicio:c_final])
    
    # Como recorremos las preguntas por filas el orden queda de la forma: 
    # [pregunta1, pregunta6, pregunta2, pregunta7, pregunta3, pregunta8...]

    # Por lo que debemos ordenarlas
    # Los indices pares contienen las 5 primeras preguntas y los impares las 5 ultimas preguntas.

    for i in range(0, len(preguntas), 2):
        preguntas_ord.append(preguntas[i])

    for i in range(1, len(preguntas), 2):
        preguntas_ord.append(preguntas[i])

    #Ploteo
    if plot:
        for pregunta in preguntas_ord:
            plt.imshow(pregunta, cmap='gray')
            plt.show()

    return preguntas_ord

# ---------------------------------------Renglones------------------------------------------------------
def DetectarRenglones(preguntas):

    renglones = []

    for pregunta in preguntas:

        pregunta_umbralizada = pregunta.copy()

        # Umbralizamos de forma que solo sobreviva el guion de la respuesta

        pregunta_umbralizada[pregunta_umbralizada == 0] = 255
        pregunta_umbralizada[(pregunta_umbralizada >= 30) & (pregunta_umbralizada <= 33)] = 0
        pregunta_umbralizada[pregunta_umbralizada > 0] = 255


        # Sumamos los pixeles por fila

        renglones_rows = np.sum(pregunta_umbralizada, axis=1)
        renglones_rows = renglones_rows // 255

        # Y los que esten dentro de este umbral seran los guiones de las preguntas

        for idx, val in enumerate(renglones_rows):
            if (val <= 208) and (val >= 20):
                renglones.append(idx)
    
    return renglones

# ---------------------------------------Indices--------------------------------------------------------
def DetectarIndices(preguntas, renglones):

    indices = []

    for pregunta, renglon in zip(preguntas, renglones):

        pregunta_umbralizada =  pregunta.copy()

        # Umbralizamos de forma que nos quede una imagen binaria de la fila del renglon

        pregunta_umbralizada[pregunta_umbralizada <  126] = 0
        pregunta_umbralizada[pregunta_umbralizada >= 126] = 255
        img_renglon = pregunta_umbralizada[renglon:renglon+1]

        binaria = img_renglon == 0

        # Vemos en que parte de la fila hay cambios de intensidad
        # Esto nos da la posicion del inicio y fin de un renglon.

        a = np.diff(binaria)
        cambios = np.argwhere(a).flatten().tolist()
        cambios = np.nonzero(a)[1].tolist()

        # Descartamos el 0 porque pertenece al recuadro de la pregunta

        if 0 in cambios:
            cambios.remove(0)
        
        # Dado que el ruido producido por las letras siempre esta al principio
        # Nos quedamos con los dos ultimos cambios de intensidad
        indices.append((cambios[-2], cambios[-1]))
    
    return indices

# ---------------------------------------Correccion-----------------------------------------------------
def CorregirRespuestas(preguntas, indices, renglones):

    respuestas_examen = []
    correcion = []

    # Area de cada letra y respuestas correctas del examen
    areas_opciones = [(22, 'C'), (28, 'A'), (29,'D'), (33, 'B')]
    respuestas_correctas = ['C', 'B', 'A', 'D', 'B', 'B', 'A', 'B', 'D', 'D']


    for pregunta, renglon, indice in zip(preguntas, renglones, indices):

        # Definimos un rango aproximado de donde se encuenta la pregunta
        # Y umbralizamos de forma que nos quede una imagen binaria

        respuesta = pregunta[renglon-14:renglon, indice[0]:indice[1]].copy()
        respuesta[respuesta <= 150] = 1
        respuesta[respuesta > 150] = 255

        # Calculamos las componentes conectadas de la imagen binaria
        # Y descartamos el fondo

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(~respuesta, 2)
        stats = stats[1:]

        # Si hay una sola respuesta nos quedamos con su area.

        if len(stats) == 1:
            area = stats[0, 4]
        
        # Si hay mas de una, quiere decir que hay una multiple respuesta

        elif len(stats) > 1:
            respuestas_examen.append('Incorrecta (Multiple respuesta)')
            continue

        # En caso de no encontrar ninguna la respuesta esta en blanco

        else:
            respuestas_examen.append('Incorrecta (En blanco)')
            continue

        # Con el area de la respuesta verficiamos a que letra corresponde
        # Cada letra tiene un area especifica

        for i in areas_opciones:
            if (area == i[0]):
                respuestas_examen.append(i[1])
                break
    
    # Verificamos si la respuesta es correcta
    # El contador es para saber la pregunta unicamente

    cont = 1
    for respuesta_examen, respuestas_correcta in zip(respuestas_examen, respuestas_correctas):

        # Este primer if es para cuando la respuesta del examen es multiple o en blanco
        # Dado que el valor de la respuesta en esos caso es de:  'Incorrecta (Multiple respuesta)' o 'Incorrecta (En blanco)'

        if respuesta_examen not in respuestas_correctas:
            print(f'{cont}. {respuesta_examen}')
            correcion.append(respuesta_examen)
        
        elif respuesta_examen == respuestas_correcta:
            print(f'{cont}. Correcta')
            correcion.append('Correcta')
        
        else:
            print(f'{cont}. Incorrecta')
            correcion.append('Incorrecta')
        
        cont += 1
    
    return correcion

# ---------------------------------------Datos----------------------------------------------------------
def DetectarIndicesDatos(img, renglon, plot=False):

    # Copiamos la imagen original y obtenemos una imagen binaria con el reglon de los datos

    img_umbralizada =  img.copy()
    img_umbralizada[img_umbralizada <  126] = 0
    img_umbralizada[img_umbralizada >= 126] = 255
    img_renglon = img_umbralizada[renglon:renglon+1]

    binaria = img_renglon == 0

    # Mismo procedimiento que antes para calcular los indices de cada renglon

    a = np.diff(binaria)
    cambios = np.argwhere(a).flatten().tolist()
    cambios = np.nonzero(a)[1].tolist()

    if 0 in cambios:
        cambios.remove(0)

    # Ploteo

    if plot:
        plt.subplot(131)
        plt.imshow(img[renglon-20:renglon+1, cambios[0]:cambios[1]], cmap='gray')
        plt.subplot(132)
        plt.imshow(img[renglon-20:renglon+1, cambios[2]:cambios[3]], cmap='gray')
        plt.subplot(133)
        plt.imshow(img[renglon-20:renglon+1, cambios[4]:cambios[5]], cmap='gray')
        plt.show()
    
    # Como siempre hay unicamente tres datos los guardo de esta forma
    
    indices = [(cambios[0],cambios[1]), (cambios[2],cambios[3]), (cambios[4],cambios[5])]

    return indices


def CorregirDatos(img, indicesDatos, datos_row):

    # Variable que indica si hay un espacio o no.
    espacio = False

    for indice in indicesDatos:

        # Para cada dato obtenemos sus stats
    
        datos = img[datos_row-20:datos_row, indice[0]:indice[1]].copy()
        datos[datos <= 150] = 1
        datos[datos > 150] = 255

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(~datos, 2)

        # Dependiendo de la iteracion instanciamos una variable diferente

        iteracion = indicesDatos.index(indice)

        # En el caso del nombre tambien guardo el crop de la imagen

        if iteracion == 0:
            nombre = stats[1:]
            campo_nombre = img[datos_row-20:datos_row, indice[0]:indice[1]].copy()
        
        if iteracion == 1:
            fecha = stats[1:]
        
        if iteracion == 2:
            clase = stats[1:]
    
    # Para calcular los espacios la distancia entre el borde derecho de una letra 
    # Y borde el izquierdo de la siguiente debe ser mayor a un umbral
    
    for i in range(len(nombre)-1):

        x_actual = nombre[i, 0]
        ancho_actual = nombre[i, 2]
        borde_derecho_actual = x_actual + ancho_actual

        x_siguiente = nombre[i + 1, 0]
        distancia = x_siguiente - borde_derecho_actual

        if distancia >= 5:
            espacio = True


    if len(nombre) <= 25 and espacio:
        print('Nombre: OK')
    else:
        print('Nombre: MAL')
    
    if len(fecha) == 8:
        print('Fecha: OK')
    else:
        print('Fecha: MAL')

    if len(clase) == 1:
        print('Clase: OK')
    else:
        print('Clase: MAL')
    
    return campo_nombre
    

def MostrarCorreciones(correcion,  campo_nombre):
    
    # Copiamos el crop del nombre, 
    # Si hay al menos 6 respuestas correctas agregamos al crop un indicativo
    # Lo mismo en caso contrario

    nombre_copia = campo_nombre.copy()

    if correcion.count('Correcta') >= 6:
        cv2.putText(nombre_copia, ':)', (180, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1, cv2.LINE_AA)
    
    else:
        cv2.putText(nombre_copia, ':(', (180, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1, cv2.LINE_AA)
    
    return nombre_copia

# Correcion de todos los examenes

lista_img = []

for id in range(1,6):

    ruta = f'examen_{id}.png'
    img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

    box_rows, box_cols, datos_row = DetectarLineas(img, plot=False)
    preguntas = DetectarPreguntas(img, box_rows, box_cols, plot=False)

    renglones = DetectarRenglones(preguntas)
    indices = DetectarIndices(preguntas, renglones)

    print(f' \nExamen Nro {id}. \n')
    correcion = CorregirRespuestas(preguntas, indices, renglones)

    indicesDatos = DetectarIndicesDatos(img, datos_row, plot=False)
    campo_nombre = CorregirDatos(img, indicesDatos, datos_row)
    nombre_copia = MostrarCorreciones(correcion,  campo_nombre)

    lista_img.append(nombre_copia)


fig, axs = plt.subplots(5, 1)
axs = axs.ravel()

for i in range(len(lista_img)):
    axs[i].imshow(lista_img[i], cmap='gray')
    axs[i].axis('off')  

plt.tight_layout()
plt.show()
