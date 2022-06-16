# Tarea Semana 16 Física Computacional 1
# Mauricio Bolívar González y Andrea De La Peña Castro

########################## Bibliotecas ###############################

import numpy as np
import matplotlib.pyplot as plt

# Parte 2: Algorítmo Genético Modificado
############################################# Funciones ###################################################


def DistanciaMinima(pcoordenadax, pcoordenaday, pcoordenadasCiudades):
    """
    Función que permite encontrar la ciudad más cercana
    :param pcoordenadax: coordenada eje x de la ciudad a la cual se le desea encontrar la ciudad más cercana
    :param pcoordenaday: coordenada eje y de la ciudad a la cual se le desea encontrar la ciudad más cercana
    :param pcoordenadasCiudades: coordenadas de las ciudades
    :return: devuelve la posición de la ciudad más cercana
    """
    # Valor arbitrario inicial para ir disminuyendo la distancia mínima
    parámetro_dist = 100000
    coordenadasDisMin = 100
    # Se recorre la lista de coordenadas de ciudades
    for i in pcoordenadasCiudades:
        coordenadasX = i[0]
        coordenadasY = i[1]
        # Distancia entre ciudades
        distanciax = coordenadasX - pcoordenadax
        distanciay = coordenadasY - pcoordenaday
        distancia = np.sqrt(distanciax ** 2 + distanciay ** 2)
        # Se cambia la distancia mínima cada vez que hay una menor
        if distancia < parámetro_dist and distancia != 0:
            parámetro_dist = distancia
            coordenadasDisMin = coordenadas.index(i)

    return coordenadasDisMin



def InicializacionModificada(ppoblacion, pciudades, pcoordenadasCiudades, probMutacion):
    """
    Función de inicialización del algoritmo genético estándar para un arreglo ciudades
    :param ppoblacion: tamaño de la población
    :param pciudades: cantidad de ciudades
    :param pcoordenadasCiudades: coordenadas de las ciudades
    :param probMutacion: probailidad de aceptación de la mutación
    :return: arreglo de permutaciones del orden de las ciudades (codificación)
    """
    poblacion = []
    for i in range(ppoblacion):
        # Se escoge una ciudad inicial de manera aleatoria
        ciud_inicial = np.random.randint(0, pciudades)
        # Se inicializa una lista de ciudades y de coordenadas
        ciudades = []
        lista_coordenadas = []

        lista_coordenadas.append(pcoordenadasCiudades[ciud_inicial])
        ncoordenadas = pcoordenadasCiudades.copy()
        # De la lista se excluye la coordenada de la ciudad inicial
        ncoordenadas.pop(ciud_inicial)
        # Se crea un ciclo que se generará mientras hayan más de 0 coordenadas por recorrer para el vendedor
        while len(ncoordenadas) > 0:
            posxi = lista_coordenadas[-1][0]
            posyi = lista_coordenadas[-1][1]
            ciud_siguiente = DistanciaMinima(posxi, posyi, ncoordenadas)
            print(ciud_siguiente)
            lista_coordenadas.append(ncoordenadas[ciud_siguiente])
            coordenadas.pop(ciud_siguiente)
        for j in lista_coordenadas:
            ciudad_j = pcoordenadasCiudades.index(j)
            ciudades.append(ciudad_j)
        poblacion.append(ciudades)
    # Se recorre el largo de la población a partir de 1 para no mutar el primer individuo de la població
    for k in range(1, len(poblacion)):
        # Se designa el cromosoma como la entrada k de la población
        cromosoma = poblacion[k]
        cromosoma_mutado = OperadorMutacion(cromosoma, probMutacion, pciudades)
        poblacion[k] = cromosoma_mutado
    return poblacion


def CalcDistancia(permutacionCiudades, pcoordenadasCiudades, pciudades):
    """
    Función que calcula la distancia recorrida por el vendedor ambulante
    :param permutacionCiudades: arreglo de ciudades codificadas
    :param pcoordenadasCiudades: coordenadas de las ciudades
    :param pciudades: cantidad de ciudades
    :return: el valor de ajuste como el inverso de la distancia euclidiana
    """
    dEuclidiana = 0
    coordenadasx = []
    coordenadasy = []

    for i in range(len(permutacionCiudades)):
        ciudad = int(permutacionCiudades[i])
        posicionx = pcoordenadasCiudades[ciudad][0]
        posiciony = pcoordenadasCiudades[ciudad][1]
        coordenadasx.append(posicionx)
        coordenadasy.append(posiciony)
    # Distancia entre la ciudad pasada y la actual
    for j in range(pciudades-1):
        distanciax = coordenadasx[j]-coordenadasx[j+1]
        distanciay = coordenadasy[j]-coordenadasy[j+1]
        dEuclidiana += np.sqrt(distanciax ** 2 + distanciay ** 2)
    # Distancia entre la posición final e inicial
    dFinalInicialx = coordenadasx[pciudades-1]-coordenadasx[0]
    dFinalInicialy = coordenadasy[pciudades-1]-coordenadasy[0]
    distanciaF = np.sqrt(dFinalInicialx ** 2 + dFinalInicialy ** 2)

    dEuclidiana += distanciaF

    ajuste = 1 / dEuclidiana
    return dEuclidiana, ajuste

def OperadorMutacion(permutacionCiudades, probMutacion, pciudades):
    """
    Función que muta el arreglo de las permutaciones de ciudades al intercambiar alteaoramente 2 de posición
    :param permutacionCiudades: arreglo de ciudades codificadas
    :param probMutacion: probailidad de aceptación de la mutación
    :param pciudades: cantidad de ciudades
    :return: devuelve la lista de ciudades permutadas mutadas
    """
    ciudadMutada = np.copy(permutacionCiudades)
    # Ciudades (genes) a intercambiar (mutar)
    cantMutaciones = np.random.randint(3, 10)
    for i in range(cantMutaciones):
        # Inicia en 1 para no generar cambios a la primera ciudad
        ciudad1 = np.random.randint(1, pciudades)
        ciudad2 = np.random.randint(1, pciudades)
        if np.random.random() < probMutacion:
            ciudadMutada[ciudad1] = permutacionCiudades[ciudad2]
            ciudadMutada[ciudad2] = permutacionCiudades[ciudad1]
        return ciudadMutada


def Graficar_Ajustes(pajustes_totales):
    '''
    Función para graficar el ajuste promedio de cada generación de la piblación, además
    de graficar el mejor ajuste en cada generación
    :param pajustes_totales: parámetro tipo lista que se convertira en un arreglo numpy, contiene los valores de ajuste
    de cada permutación de ciudades, para cada generación de la población.
    :return: gráfica el comportamiento
    '''
    val_ajustes = np.asarray(pajustes_totales)

    # Arreglo de los promedios para cada generación
    promedios_poblacion = np.mean(val_ajustes, 1)

    # Arreglo con los máximos ajustes en cada generación
    maximos_ajustes = np.max(val_ajustes, 1)

    # GRÁFICA:
    plt.plot(promedios_poblacion, label='ajuste promedio', c='m')
    plt.plot(maximos_ajustes, label='ajuste máximo')
    plt.title('Comparación entre valores de ajuste promedio y valores máximos de ajuste')
    plt.xlabel('Generaciones')
    plt.ylabel('Valores de ajuste')
    plt.legend(loc='best')
    plt.show()


def Calcular_Ajustes(ppoblacion, pcoordenadasCiudades, pciudades, pajustes_totales):
    """
    Función que permite calcular los ajustes para la población
    :param ppoblacion: tamaño de la población
    :param pcoordenadasCiudades: coordenadas de las ciudades
    :param pciudades: cantidad de ciudades
    :param pajustes_totales: parámetro tipo lista que se convertira en un arreglo numpy, contiene los valores de ajuste
    de cada permutación de ciudades, para cada generación de la población.
    :return: lista de valores de ajuste para cada población
    """
    lista_ajustes = []
    for i in range(len(ppoblacion)):
        permutacionCiudades = ppoblacion[i]
        longitud_euc, ajustePermutacion = CalcDistancia(permutacionCiudades, pcoordenadasCiudades, pciudades)
        # Se agregan de cada permutación de ciudades
        lista_ajustes.append(ajustePermutacion)
        # Se guarda cada lista calculada en la lista total (para todas las generaciones)
    pajustes_totales.append(lista_ajustes)
    return pajustes_totales


####################################### Código Principal ###########################################

nGeneraciones=100
nPoblacion=100 #Población de cada generación
ciudades = 100
probabilidad=0.5 #Probabilidad de mutación

#Crear las listas de almacenamiento generacional

ajustes_totales=[]
poblaciones_totales=[]

# Inicialización de ciudades y poblacion:

coordenadas = []
for i in range(1, ciudades+1):
    coordenadax = 0.1 * ((9 + (13 * i ** 2)) % 200)
    coordenaday = 0.1 * ((7 + (1327 * i)) % 200)
    coordenadas.append([coordenadax, coordenaday])

poblacion_0=InicializacionModificada(nPoblacion,ciudades,coordenadas,probabilidad)

# Agregar la poblacion actual a la lista total y calcular los ajustes de esta poblacion.
poblaciones_totales.append(poblacion_0)
Calcular_Ajustes(poblacion_0,coordenadas,ciudades,ajustes_totales)

# Ejecución del ciclo generacional

for i in range(nGeneraciones):
    poblacion_actual = poblaciones_totales[i]
    # Se recorre la población para generar mutaciones con la funcion OperadorMutacion
    for j in range(len(poblacion_actual)):
        permutacion = poblacion_actual[j]
        permutacion_mutada = OperadorMutacion(permutacion, probabilidad, ciudades)
        # Se agregan las nuevas permutaciones
        poblacion_actual[j]=permutacion_mutada
    # Se agrega la poblacion de la generacion actual a la lista total y se calcula su ajuste
    poblaciones_totales.append(poblacion_actual)
    Calcular_Ajustes(poblacion_actual,coordenadas,ciudades,ajustes_totales)

# Determinación del mejor ajuste:

ajuste_temporal=0

for i in range(nGeneraciones):
    for j in range(nPoblacion):
        #se recorre la lista de ajustes totales para todas las generaciones y todas las permutaciones de ciudades
        aj_actual = ajustes_totales[i][j]
        if aj_actual > ajuste_temporal:
            ajuste_temporal=aj_actual
            indice_imax=i
            indice_jmax=j
        else:
            pass

# Se guarda la entrada de permutaciones de ciudades con el mejor ajuste en una variable
rutaoptima= poblaciones_totales[indice_imax][indice_jmax]

print('La longitud del mejor camino es ', CalcDistancia(rutaoptima,coordenadas,ciudades)[0])

# Extracción de coordenadas a partir del orden de las ciudades a visitar:

coordenadas_ciudades=[]

for indiceCiudad in rutaoptima:
  coordenadas_ciudades.append(coordenadas[int(indiceCiudad)])

# Crear listas de coordenadas para graficar en los ejes X e Y individualmente:
coordenadasX=[]
coordenadasY=[]
for j in range(len(rutaoptima)):
    coordenadasX.append(coordenadas_ciudades[j][0])
    coordenadasY.append(coordenadas_ciudades[j][1])

# Cerrar el recorrido volviendo al punto inicial:

coordenadasX.append(coordenadasX[0])
coordenadasY.append(coordenadasY[0])

# Grafico de la ruta optima y el cambio de los ajustes con las iteraciones

plt.plot(coordenadasX,coordenadasY,'r-',label='Ruta')
plt.plot(coordenadasX,coordenadasY,'bo',label='Ciudad')
plt.title('Ruta óptima')
plt.xlabel('Coordenada X [u.l]')
plt.ylabel('Coordenada Y [u.l]')
plt.legend(loc='best')
plt.show()

Graficar_Ajustes(ajustes_totales)