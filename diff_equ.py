import numpy as np

def runge_cord(x:float, y:np.ndarray, step:float, func, start_cord:float, mode=True, *args, **kwargs)->float:
    '''
    Вычисляет след координату по Рунге-Кутты\n
    Параметры:
    -
    y - предыдущая точка\n
    x - значение аргумента в предыдущей точки, в y\n
    step - шаг сетки\n
    func - функция, определяющая производную y по x
    '''
    if len(y) < 4 or not mode:
        '''Проблеама в том, что мне нужны скорости на след координате'''
        k1 = y[-1]
        k2 = runge_skor(x + step/2, y[-1:], step/2, func, mode, **kwargs)
        k3 = runge_skor(x + step/2, y[-1:], step/2, func, mode, **kwargs)
        k4 = runge_skor(x + step, y[-1:], step, func, mode, **kwargs)
        return start_cord + step/6 *(k1 + 2*(k2 + k3) + k4)
    else:
        return start_cord + step*(55/24*y[-1] -59/24*y[-2] + 37/24*y[-3] - 9/24*y[-4])

def runge_skor(x:float, y:np.ndarray, step:float, func, mode=True, *args, **kwargs):
    '''Вычисляет скорость в след момент времени с шагом step'''
    if len(y) < 4 or not mode:
        k1 = func(x, y[-1], **kwargs)
        k2 = func(x + step/2, y[-1]+ step*k1/2, **kwargs)
        k3 = func(x + step/2, y[-1] + step*k2/2, **kwargs)
        k4 = func(x + step, y[-1] + step*k3, **kwargs)
        return y[-1] + step/6 *(k1 + 2*(k2 + k3) + k4)
    else:
        return y[-1] + step*(55/24*func(x, y[-1], **kwargs) -59/24*func(x,y[-2], **kwargs) +37/24*func(x,y[-3], **kwargs) -9/24*func(x,y[-4], **kwargs))
    
if __name__ == 'main':
    pass