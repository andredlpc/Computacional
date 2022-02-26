# Tarea 1 Física Computacional Andrea De La Peña 2018124992
#Ejercicio 2

def Funcion(pt):
    """
    Función que evalúa el valor  deseado dentro
    de la función de la distancia con respecto al tiempo,
    esta función se basa de un escenario donde se parte del
    reposo, se tiene una aceleración constantes de
    0,01 m/s^2, una distancia inicial de -5 m y una
    posición final de 0 m.
    :param pt: Parámetro del tiempo en segundos
    :return: La función devuelve la distancia en metros
    donde se encuentra para un tiempo t
    """
    funcionEv = -5 + 1/2 * 0.01 * (pt**2)
    return funcionEv

def DerivadF(pt):
    """
    Función que deriva la función de la distancia dependiente del tiempo
    utilizando la definición de la derivada, el valor de h se toma como
    una aproximación de que este tiende a 0.
    :param pt: Parámetro del tiempo en segundos
    :return: La función devuelve el valor aproximado de la derivada
    de primer orden evaluada en el valor deseado de t
    """
    h = 0.0001
    dervf = (Funcion(pt+h) - Funcion(pt-h)) / (2*h)
    return dervf

def Resultado(px_0, pn):
    """
    Función que ejecuta el método de Newton Raphson, esto por medio de
    un ciclo que empieza con el valor deseado inicial para aproximar
    el tiempo y se va mejorando la aproximación cuantas veces se quiera.
    :param px_0: Parámetro del primer valor para aproximar el valor del
    tiempo
    :param pn: Parámetro de la cantidad de veces que se desea mejorar
    la aproximación
    :return: Esta función devuelve un valor aproximado del tiempo
    que se tiene en una posición de 0 m donde se parte del reposo
    y se acelera constantemente a 0,01 m/s^2 y se empieza de una
    posición de -5 m.
    """
    for i in range(1, pn + 1):
        xi = px_0 - (Funcion(px_0)/DerivadF(px_0))
        px_0 = xi
    return xi

x_0 = 1 #aproximación inicial
nAprox = 12 #cantidad de aproximaciones

print(Resultado(x_0, nAprox))

