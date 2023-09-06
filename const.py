from numpy import exp, sin, cos, sqrt
import numpy as np

def field(x1, *args, **kwargs):
    return sqrt(abs(x1)) * x1 * (2 + sin(x1))*0.05

def x1(t:float, a:float, m:float, u:float, cos_a:float, *args, **kwargs)->float:
    if a != 0:
        return m/a*u*cos_a*(1 -exp(-a/m*t))
    else:
        return u*cos_a*t

def x2(t:float, a:float, m:float, u:float, sin_a:float, g:float, *args, **kwargs)->float:
    if a != 0:
        return m/a*(g*m/a + u*sin_a - g*t - exp(-a/m*t)*(g*m/a +u*sin_a))
    else:
        return -g *t *t/2 + u*sin_a*t
    
def ux1(t: float, a:float, m:float, u:float, cos_a:float, *args, **kwargs) -> float: # Уравнение скорости по x
    if a != 0:
        return exp(-a/m*t)*u*cos_a
    else:
        return u * cos_a


def ux2(t: float, a:float, m:float, u:float, sin_a:float, g:float, *args, **kwargs) -> float: # Уравнение скорости по y
    if a !=0:
        return exp(-a/m*t)*(g*m/a + u*sin_a) - g*m/a
    else:
        return -g*t + u*sin_a
    
def x1_usk(t:float, x:float, a:float, m:float, *args, **kwargs):
    return -x*a/m

def x2_usk(t:float, x:float, a:float, m:float, g:float, *args, **kwargs):
    return -x*a/m - g

def psi(x_array: np.ndarray, cix: float, i: int, x: float) -> float:
    '''
    Вычисление одного из членов интерполяционного полинома\n
    Параметры:
    -
    x_array - набор узлов\n
    cix - i-ый элемент базиса\n
    i - номер\n
    x - точка, в которой вычисляется значение
    '''
    result = cix
    for j, xj in enumerate(x_array):
        if (j != i):
            result = result * (x-xj)
    return result


def ci(xj: np.ndarray, x: float) -> float:
    '''
    Вычислегие i-го элемента константной части базиса Лагранжа\n
    Параметры:
    -
    xj - набор узлов\n
    x - i-ый узел
    '''
    c = 1
    for xi in xj:
        if xi != x:
            c = c * 1/(x - xi)
    return c


def y_x(x:float, yi: np.ndarray, xi: np.ndarray, cix:np.ndarray, *args, **kwargs) -> float:
    '''
    Создание и вычисление интерполяционного полинома Лагранжа\n
    Параметры:
    -
    yi - набор значений функции\n
    xi - набор узлов\n
    cix - набор константных частей базиса\n
    x - в какой точке вычисляется полином
    '''
    fi = np.array(list(), dtype=np.float128)
    for i in range(len(yi)):
        fi = np.append(fi, psi(xi, cix[i], i, x))
    return (yi*fi).sum()

if __name__ == "__main__":
    setting = {
        'func': lambda t: t*t,
        'xi': [0, 1, 2],
        'cix': [ci([0, 1, 2], i) for i in range(3)]
    }
    setting['yi'] = [setting['func'](t) for t in setting['xi']]
    
    max_error = 0
    
    for i in np.arange(0, 2, 0.5):
        error = abs(setting['func'](i) - y_x(i, **setting))
        if error > max_error:
            max_error = error
    print(max_error)