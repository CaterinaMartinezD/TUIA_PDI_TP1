# Procesamiento de Imágenes (PDI)
## TRABAJO PRÁCTICO N° 1 - Año 2024
**Integrantes:**

- Nombre: Zahradnicek, Ezequiel.
- Nombre: Grimaldi, Damián.
- Nombre: Martinez Dufour, Caterina.

### Introducción:
Este repositorio cuenta con la resolución del primer trabajo práctico de la asignatura “Procesamiento de imágenes” de la Tecnicatura en Inteligencia Artificial. Se implementan diferentes técnicas de procesamiento para llegar a la resolución de los problemas planteados. En este informe se describirán las instrucciones necesarias para realizar la ejecución del código correctamente.

### Problema 1 - Ecualización local de histograma:
Este problema consiste en utilizar el algoritmo de ecualización local del histograma el cual se define mediante una ventana que se desplaza pixel a pixel por la imagen. En cada posición de la ventana se calcula el histograma y se ajusta el valor del píxel central, esto genera una transformación local. Por último, se desplaza la ventana un píxel hacia el costado y repite el proceso en toda la imagen.

### Ejecución:
Se debe acceder al archivo denominado “ejercicio1.py” y contar con el archivo “Imagen_con_detalles_escondidos.tif”. Este código tiene como objetivo visualizar las imágenes ocultas que se encuentran en los cuadrados negros de una imagen dada.

Para lograr esto, es necesario leer la imagen “Imagen_con_detalles_escondidos.tif” y emplear una función llamada “equalizacion_local”. Esta función se encargará de realizar una ecualización local de la imagen proporcionada y tiene tres parámetros: “img”, que es la imagen que se va a procesar; “tamaño_ventana”, que define el tamaño de la ventana utilizada para la ecualización; y “truncate”. Si truncate es verdadero, ajusta ciertos valores de píxeles antes de aplicar la ecualización.

El procedimiento consiste en leer la imagen Imagen_con_detalles_escondidos.tif, aplicar la función equalizacion_local para resaltar los detalles escondidos y visualizar la imagen resultante para observar los detalles que se revelan en los cuadrados negros. En este código se implementan ejemplos de cómo se ejecuta el código con diferentes tamaños de ventana y aplicando la opción de truncamiento de píxeles.

### Problema 2 - Corrección de múltiple choice:
Este problema contiene una serie de exámenes resueltos en formato imagen y se debe realizar una corrección automática. Para ello se brinda una lista de las respuestas correctas que pueden ser entre A, B, C y D. su criterio de corrección será la siguiente:

- Si una respuesta contiene más de una opción seleccionada, se considera incorrecta.
- Si una respuesta no tiene ninguna opción marcada, también se considera incorrecta.

El algoritmo a desarrollar debe tener en cuenta los siguientes puntos:

- Tomar únicamente como entrada la imagen de un examen y mostrar por pantalla cuáles de las respuestas son correctas y cuáles incorrectas.
- Validar los datos del encabezado y mostrar por pantalla si:
  - Name: debe contener al menos 2 palabras y no más de 25 caracteres.
  - Date: deben ser 8 caracteres formando una sola palabra.
  - Class: un único carácter.

Utilice el algoritmo desarrollado para evaluar las imágenes de exámenes resueltos (archivos examen_.png) e informe cada resultado obtenido.

Generar una imagen de salida informando los alumnos que han aprobado el examen (con al menos 6 respuestas correctas) y aquellos alumnos que no.

### Ejecución:
Se debera acceder al archivo llamado “ejercicio2.py” y tener los archivos llamados “examen_1.png”, “examen_2.png”, “examen_3.png”, “examen_4.png” y “examen_5.png”. En este código se presenta toda la resolución del ejercicio 2 y se utilizara varias funciones para resolver los problemas establecidos:

En este código podremos encontrar 8 funciones, las cuales explicaré a continuación:

#### Función “DetectarLineas()”: 
Esta función detecta las líneas horizontales y verticales. Calcula la suma de los píxeles en cada fila y columna para obtener el área donde se pueden encontrar líneas. Luego, al obtener un número muy elevado, se realiza una división por 255 para trabajar con cifras más pequeñas. Se realiza un filtrado de líneas determinando a través de un umbral cuáles sumas son menores o iguales a este, indicando que hay líneas existentes.

La primera fila contiene los datos del estudiante y se almacena para usar en un ejercicio más adelante. Por último devuelve las filas y columnas detectadas además de los datos del estudiante.

#### Función “DetectarPreguntas()”: 
Esta función se encarga de extraer las preguntas del examen utilizando las filas y columnas obtenidas en la función anterior. Se recorre por fila y columna los datos de interés y se obtienen las preguntas, luego se agregan a la lista “preguntas_ord” creada anteriormente.

Cómo se obtienen las preguntas por fila, el orden queda [pregunta 1, pregunta 6, pregunta 2, pregunta 7, pregunta 3, pregunta 8...], es por eso que se deben ordenar. Para ello se toman los índices pares que contienen las 5 primeras preguntas y los impares las últimas 5 preguntas. Esta función devuelve las preguntas ordenadas.

#### Función “DetectarReglones()”: 
Esta función se encarga de obtener los renglones donde se encuentra la respuesta de cada pregunta. Crea una lista vacía llamada "renglones" y umbraliza la imagen de forma que solamente quede el guión de la respuesta. La imagen al realizar esto quedará con ruido y obtendrá el renglón deseado.

Se suma los píxeles por fila y los que estén dentro del umbral serán considerados renglones y se agregarán a la lista. Devuelve los renglones obtenidos.

#### Función “Detectar_Indices()”: 
Se encarga de obtener los índices de las respuestas. Crea una lista para almacenar los índices y aplica un umbral a la fila correspondiente, generando una imagen binaria para detectar cambios de intensidad. Estos cambios indican el inicio y fin de cada renglón.

Se elimina el valor obtenido en la posición cero ya que este proviene del recuadro de la pregunta. Luego, se agrega a la lista índices los dos últimos cambios de intensidad debido a que el ruido producido por las letras siempre está al principio. Los índices obtenidos se almacenan y se devuelven.

#### Función “CorregirRespuestas()”: 
Esta función corrige los resultados de las respuestas del examen y almacena las correcciones en una lista. Extrae el área de cada respuesta, crea una imagen binaria y calcula las componentes conectadas. Si hay más de una respuesta, se considera incorrecta; si no hay respuestas, se registra como en blanco. Se verifica cuál es la respuesta correcta y se almacena.

Luego, las respuestas que poseen solo una letra, se verifica qué letra está viendo su área y se almacena la respuesta. Por último, se inicia un contador para ingresar las respuestas obtenidas en orden. Devuelve la corrección final.

#### Función “DetectarIndicesDatos()”: 
Esta función identifica y extrae los datos del estudiante, el cual copia la imagen original y obtiene los datos de una imagen binaria con el renglón de los datos y calcula los índices de cada uno. Devuelve el índice con 3 datos (nombre, fecha y clase).

#### Función “CorregirDatos()”: 
Esta función tiene como objetivo verificar la validez de los datos extraídos de la imagen del examen y si es necesario corregir o ajustar los resultados. Para cada índice en “indicesDatos”, se extraen las características de los datos (nombre, fecha, clase) de la imagen usando el método de componentes conectados. Dependiendo de la iteración, se almacenan las estadísticas de los componentes detectados en variables separadas (nombre, fecha, clase).

Para el nombre, se guarda una copia del segmento de la imagen correspondiente a ese campo para usar más tarde. Para verificar si una letra tiene espacio, se calcula la distancia entre el borde derecho de una letra y el borde izquierdo de la siguiente, debe ser mayor a un umbral. Por último se devuelve el campo nombre.

#### Función “MostrarCorreciones()”: 
Muestra los resultados de las correcciones del examen de cada estudiante. Verifica cuántas respuestas han sido calificadas como correctas; si hay al menos seis respuestas correctas, agrega un ":)". De lo contrario, agrega un ":(". Devuelve la imagen del nombre con el texto agregado.

### En el último fragmento del código:
Se inicializa “lista_img” y se itera sobre cinco exámenes. Para cada uno, se carga la imagen, se detectan líneas, preguntas y renglones. Se corrigen las respuestas e identifica los datos del estudiante. La imagen del nombre se modifica con una carita feliz o triste, según la cantidad de respuestas correctas. Finalmente, se muestran todas las imágenes corregidas.
