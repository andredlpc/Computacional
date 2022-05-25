# Tecnológico de Costa Rica | Semestre I 2022
# Tarea Semana 13 Física Computacional I
# Mauricio Bolívar González 2018132999
# Andrea De La Peña Castro 2018124992

import numpy as np
import matplotlib.pyplot as plt


nSpines = 100
kbT = 1
nPasos = 12000
corridas = 20
ejeTemp = np.linspace(0.1, 5, num=12)


def SumaEnergia(pArreglo, pPaso):
    """
    Función que realiza la suma necesaria de la relación para
    encontrar el resultado de la energía
    :param pArreglo: arreglo que contiene los valores de los espines
    para cada paso correspondiente
    :param pPaso: paso en el tiempo donde se va a calcular la suma
    :return: devuelve el valor de la suma de la relación de energía
    """
    valorextremo = pArreglo[pPaso, 0]*pArreglo[pPaso, nSpines-1]
    sumatoria = valorextremo
    for j in range(0, nSpines-1):
        valorj = pArreglo[pPaso, j]*pArreglo[pPaso, j+1]
        sumatoria += valorj
    return sumatoria


def SumaMag(pArreglo, pPaso):
    """
    Función que calcula el valor de la magnetización
    :param pArreglo: arreglo que contiene los valores de los espines
    para cada paso correspondiente
    :param pPaso: paso en el tiempo donde se va a calcular la suma
    :return: devuelve el valor absoluto de la suma que corresponde
    al valor de la magnetización
    """
    sumatoria = 0
    for j in range(0, nSpines):
        sumatoria += pArreglo[pPaso, j]
    return abs(sumatoria)


def Simulacion(pArreglo, pListaE, pListaM, pKBT):
    """
    Función que corre el algoritmo de metrópolis
    :param pArreglo: arreglo que contiene los valores de los espines
    para cada paso correspondiente
    :param pListaE: arreglo con los valores de energía que se van actualizando
    :param pListaM: arreglo con los valores de magnetización que se van actualizando
    :param pKBT: valor de la constante de Boltzman por la temperatura
    :return: modifica las listas y devuelve el lugar dentro del arreglo del último cálculo
    """
    kcontador = 0
    while kcontador < nPasos - 1:
        # Actualizar los siguientes valores:
        pArreglo[kcontador + 1, :] = pArreglo[kcontador, :]
        # Calcular energia actual y nueva para un cambio aleatorio:
        energiaactual = -1 * SumaEnergia(pArreglo, kcontador)
        val_aleatorio = np.random.randint(nSpines)
        valorOG = pArreglo[kcontador, val_aleatorio]
        pArreglo[kcontador, val_aleatorio] = -1 * valorOG
        energianueva = -1 * SumaEnergia(pArreglo, kcontador)
        pListaM[kcontador] = SumaMag(pArreglo, kcontador)
        pListaE[kcontador] = energiaactual

        if energianueva > energiaactual:
            if np.random.random() < np.exp(-(energianueva - energiaactual) / pKBT):
                pArreglo[kcontador + 1, val_aleatorio] = pArreglo[kcontador, val_aleatorio]
            else:
                pArreglo[kcontador + 1, val_aleatorio] = -1 * pArreglo[kcontador, val_aleatorio]
        else:
            pArreglo[kcontador + 1, val_aleatorio] = pArreglo[kcontador, val_aleatorio]

        pArreglo[kcontador, val_aleatorio] = valorOG
        kcontador += 1
    return kcontador


def ModeloIsing(pArreglo, pOpcion):
    """
    Función que realiza el algoritmo de Metrópoli para diferentes opciones a elegir
    de la condición inicial de los espines
    :param pArreglo: arreglo que contiene los valores de los espines
    para cada paso correspondiente
    :param pOpcion: condición inicial deseada
    :return: devuelve el comportamiento del sistema (Energía Interna y Magnetización)
    a lo largo del tiempo de manera gráfica
    """
    if pOpcion == 1:
        for i in range(0, nSpines):
            randnum = np.random.uniform(0, 1)
            if randnum < 0.5:
                pArreglo[0, i] = -0.5
            else:
                pArreglo[0, i] = 0.5
    elif pOpcion == 2:
        for i in range(0, nSpines):
            pArreglo[0, i] = 0.5

    elif pOpcion == 3:
        for i in range(0, nSpines):
            pArreglo[0, i] = -0.5

    listaEnergias = np.zeros(nPasos)
    listaMagnetizacion = np.zeros(nPasos)
    conteoEnergias = np.zeros(nPasos - 2000)
    conteoMagnetizacion = np.zeros(nPasos - 2000)

    indice = Simulacion(pArreglo, listaEnergias, listaMagnetizacion, kbT)

    listaMagnetizacion[indice] = SumaMag(arreglo_electrones, indice)
    listaEnergias[-1] = listaEnergias[indice - 1]

    for k in range(0, nPasos - 2000):
        conteoEnergias[k] = listaEnergias[k + 2000]
        conteoMagnetizacion[k] = listaMagnetizacion[k + 2000]

    # Calculo de promedios
    promEnergia = 1 / (nPasos - 2000) * (np.sum(conteoEnergias))  # Primer calculo de <E>=U
    promMagnetizacion = 1 / (nPasos - 2000) * (np.sum(conteoMagnetizacion))  # Primer calculo de <M>

    # Graficar

    grafico = np.swapaxes(pArreglo, 0, 1)
    plt.imshow(grafico, cmap=plt.cm.jet, aspect='auto')
    plt.colorbar()
    plt.title('Estados de ' + str(nSpines) + ' espines')
    plt.xlabel('Pasos')
    plt.ylabel('Espin')
    plt.show()

    tiempo = np.arange(0, nPasos, 1)

    plt.plot(tiempo, listaEnergias)
    plt.title('Energía de cada configuración a lo largo del tiempo')
    plt.xlabel('Pasos')
    plt.ylabel('Energía $E_{aj}$')
    plt.axhline(y=promEnergia, color='red', linestyle='-.', label='Promedio Energía')
    plt.legend(loc='lower right')
    plt.show()

    plt.plot(tiempo, listaMagnetizacion)
    plt.title('Magnetizacion')
    plt.xlabel('Pasos')
    plt.ylabel('Magnetizacion $M_j$')
    plt.axhline(y=promMagnetizacion, color='red', linestyle='-.', label='Promedio Magentizacion')
    plt.legend(loc='upper right')
    plt.show()


def Ensamble(pArreglo, pOpcion):
    """
    Función que realiza el algoritmo de Metrópoli 20 veces para diferentes opciones a elegir
    de la condición inicial de los espines
    :param pArreglo: arreglo que contiene los valores de los espines
    para cada paso correspondiente
    :param pOpcion: condición inicial deseada
    :return: el promedio del ensamble de las variables de Energía Interna y Magnetización
    3medidas del sistema
    """
    conteoPromediosE = np.zeros(corridas)
    conteoPromediosM = np.zeros(corridas)
    for conteo in range(0, corridas):
        if pOpcion == 1:
            for i in range(0, nSpines):
                randnum = np.random.uniform(0, 1)
                if randnum < 0.5:
                    pArreglo[0, i] = -0.5
                else:
                    pArreglo[0, i] = 0.5
        elif pOpcion == 2:
            for i in range(0, nSpines):
                pArreglo[0, i] = 0.5

        elif pOpcion == 3:
            for i in range(0, nSpines):
                pArreglo[0, i] = -0.5

        listaEnergias = np.zeros(nPasos)
        listaMagnetizacion = np.zeros(nPasos)
        conteoEnergias = np.zeros(nPasos - 2000)
        conteoMagnetizacion = np.zeros(nPasos - 2000)

        indice = Simulacion(pArreglo, listaEnergias, listaMagnetizacion, kbT)

        listaMagnetizacion[indice] = SumaMag(arreglo_electrones, indice)
        listaEnergias[-1] = listaEnergias[indice - 1]

        for k in range(0, nPasos - 2000):
            conteoEnergias[k] = listaEnergias[k + 2000]
            conteoMagnetizacion[k] = listaMagnetizacion[k + 2000]

        # Calculo de promedios
        promEnergia = 1 / (nPasos - 2000) * (np.sum(conteoEnergias))  # Primer calculo de <E>=U
        promMagnetizacion = 1 / (nPasos - 2000) * (np.sum(conteoMagnetizacion))  # Primer calculo de <M>

        conteoPromediosE[conteo] = promEnergia
        conteoPromediosM[conteo] = promMagnetizacion

    promGeneralE = 1 / corridas * (np.sum(conteoPromediosE))
    promGeneralM = 1 / corridas * (np.sum(conteoPromediosM))

    print('El promedio para E es: ', round(promGeneralE, 3))
    print('El promedio para M es: ', round(promGeneralM, 3))

    plt.plot(np.arange(0, corridas, 1), conteoPromediosE)
    plt.title('Energía promedio de cada corrida')
    plt.xlabel('# Corrida')
    plt.ylabel('<E>')
    plt.show()

    plt.plot(np.arange(0, corridas, 1), conteoPromediosM)
    plt.title('Magnetizacion promedio de cada corrida')
    plt.xlabel('# Corrida')
    plt.ylabel('<M>')
    plt.show()


def Propiedades(pArreglo, pOpcion):
    """
    Función que corre el algoritmo por medio de la función de Ensable para dostintos valores
    de temperatura y compara el comportamiento del sistema con las predicciones analíticas
    :param pArreglo: arreglo que contiene los valores de los espines
    para cada paso correspondiente
    :param pOpcion: condición inicial deseada
    :return: devuelve la comparación de la simulación (Energía Interna, Magnetización y Calor Específico)
    con las predicciones analíticas
    """
    arregloUinterna = np.zeros_like(ejeTemp)
    arregloM = np.zeros_like(ejeTemp)
    arregloC = np.zeros_like(ejeTemp)
    for numero in range(0, len(ejeTemp)):
        conteoPromediosE = np.zeros(corridas)
        conteoPromediosM = np.zeros(corridas)
        for conteo in range(0, corridas):
            if pOpcion == 1:
                for i in range(0, nSpines):
                    randnum = np.random.uniform(0, 1)
                    if randnum < 0.5:
                        pArreglo[0, i] = -0.5
                    else:
                        pArreglo[0, i] = 0.5
            elif pOpcion == 2:
                for i in range(0, nSpines):
                    pArreglo[0, i] = 0.5

            elif pOpcion == 3:
                for i in range(0, nSpines):
                    pArreglo[0, i] = -0.5

            listaEnergias = np.zeros(nPasos)
            listaMagnetizacion = np.zeros(nPasos)
            conteoEnergias = np.zeros(nPasos - 2000)
            conteoMagnetizacion = np.zeros(nPasos - 2000)

            indice = Simulacion(pArreglo, listaEnergias, listaMagnetizacion, ejeTemp[numero])

            listaMagnetizacion[indice] = SumaMag(arreglo_electrones, indice)
            listaEnergias[-1] = listaEnergias[indice - 1]

            for k in range(0, nPasos - 2000):
                conteoEnergias[k] = listaEnergias[k + 2000]
                conteoMagnetizacion[k] = listaMagnetizacion[k + 2000]

            # Cálculo de promedios
            promEnergia = 1 / (nPasos - 2000) * (np.sum(conteoEnergias))  # Primer calculo de <E>=U
            promMagnetizacion = 1 / (nPasos - 2000) * (np.sum(conteoMagnetizacion))  # Primer calculo de <M>

            conteoPromediosE[conteo] = promEnergia
            conteoPromediosM[conteo] = promMagnetizacion

        promGeneralE = 1 / corridas * (np.sum(conteoPromediosE))
        promGeneralM = 1 / corridas * (np.sum(conteoPromediosM))

        uSQC = promGeneralE ** 2
        u2C = 1 / corridas * (np.sum(np.square(conteoPromediosE)))
        promGeneralC = ((u2C - uSQC) / (ejeTemp[numero] ** 2)) * 1 / (corridas ** 2) * 10

        # promGeneralC=1/corridas*(np.sum(conteoPromediosC))

        arregloUinterna[numero] = promGeneralE
        arregloM[numero] = promGeneralM
        arregloC[numero] = promGeneralC

    plt.plot(ejeTemp, arregloUinterna)
    ejeY1 = -1 * nSpines * np.tanh(1 / ejeTemp)
    plt.plot(ejeTemp, ejeY1, label='Teorico', color='red')
    plt.title('U vs kbT')
    plt.xlabel('kbT')
    plt.ylabel('U')
    plt.legend(loc='upper left')
    plt.show()

    plt.plot(ejeTemp, arregloM)
    ejeY2 = 1 * (nSpines * np.exp(1 / ejeTemp) * np.sinh(1 / ejeTemp)) / np.sqrt(
        np.exp(2 / ejeTemp) * np.sinh(1 / ejeTemp) ** 2 + np.exp(-2 / ejeTemp))
    plt.plot(ejeTemp, ejeY2, label='Teorico', color='red')
    plt.title('M vs kbT')
    plt.xlabel('kbT')
    plt.ylabel('M')
    plt.legend(loc='upper right')
    plt.show()

    plt.plot(ejeTemp, arregloC)

    ejeY3 = 1 / (ejeTemp ** 2 * (np.cosh(1 / ejeTemp) ** 2))
    plt.plot(ejeTemp, ejeY3, label='Teorico', color='red')

    plt.title('C vs kbT')
    plt.xlabel('kbT')
    plt.ylabel('C')
    plt.legend(loc='upper right')
    plt.show()


seccionTarea = int(input('Escoja la sección donde quiere obtener los resultados: \n 1. Modelo de Ising (Seccion 1.1.), '
                         '\n 2. Ensamble de simulación (Sección 1.2. puntos a-c), \n '
                         '3. Propiedades termodinamicas (Sección 1.2. puntos d-f): '))

opcionincial = int(input('Escoja el estado inicial (1. Caliente, 2. Spin arriba, 3. Spin abajo): '))

arreglo_electrones = np.zeros((nPasos, nSpines))

if seccionTarea == 1:
    ModeloIsing(arreglo_electrones, opcionincial)
elif seccionTarea == 2:
    Ensamble(arreglo_electrones, opcionincial)
elif seccionTarea == 3:
    Propiedades(arreglo_electrones, opcionincial)
