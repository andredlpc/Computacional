# Tarea 1 Física Computacional Andrea De La Peña 2018124992
# Ejercicio 1

a = 0 #límite inferior de la integral
b = 100 #límite superior de la integral

n = 2 #cantidad de puntos

def Funcion(pt):
    """
    Función que evalúa el valor deseado del tiempo
    para obtener su respectiva posición en ese momento
    para una rapidez inicial de 0,05 m/s, una rapidez
    final de 1 m/s a los 100 s con aceleración constante.
    :param pt: Parámetro tiempo en segundos
    :return: Esta función devuelve el valor de la
    posición en el tiempo deseado
    """
    aceleracion = (1-0.5) / 100
    funcionEv = 0.5 + aceleracion *pt
    return funcionEv


def Resultado(pa, pb, pn):
    """
    Función que utiliza el método de Integración Numérica del Trapezio
    para encontrar el resultado del desplazamiento de un móvil en un
    intervalo específico de tiempo.
    :param pa: Parámetro del valor inferior del intervalo del tiempo en s
    :param pb: Parámetro del valor superior del intervalo del tiempo en s
    :param pn: Parámetro de la cantidad de puntos deseados para aplicar
    el método de integración del Trapezio
    :return: Esta función devuelve el valor aproximado del desplazamiento
    dentro de un intervalo de tiempo específico para un móvil con
    aceleración constante con una rapidez inicial de 0,05 m/s y una
    rapidez final de 1 m/s
    """
    h = (pb - pa) / (pn - 1)
    suma = 0
    for i in range(1, pn + 1):
        xi = pa + (i - 1) * h
        if i == 1 or i == pn:
            suma = Funcion(xi) * (h/2) + suma
        else:
            suma = Funcion(xi) * h + suma
    print(suma)


Resultado(a, b, n)

