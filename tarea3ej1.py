import numpy as np
import scipy.integrate

def F(t, v):
    '''Esta función corresponde al lado derecho de la EDO de primer orden v'=f(v, t)

    Parámetros de la función
    ------------------------
    v : función de la variable t del lado derecho de la EDO
    t : variable t sobre la que se desarrolla la EDO

    Salida de la función
    --------------------
    valorf : valor de la función f(v, t) evaluada en t
    '''

    # Se define la función f(v, t)
    valorf = (rho - rhoF)*g/rho - alfa*v
    return valorf


#Se define los valores de t de interés y el valor inicial de v(t)
#El intervalo de valores de t se extiende desde ti hasta tf y el número de valores es n
ti = 0.0
tf = 1.0
intIntegracion = [ti, tf]
n = int(1/0.05)
t = np.linspace(ti, tf, n)
v0 = 0.0

#Parámetros conocidos para el caso físico específico
rho = 7.874
rhoF = 1.260
g = 9.8
alfa = 10

#Solución de la EDO
vSol = scipy.integrate.solve_ivp(F, intIntegracion, [v0], method='RK45', t_eval=t)

print(vSol.y[0])



