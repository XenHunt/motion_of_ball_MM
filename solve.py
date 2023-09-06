from sekush import sekush
from const import field
import numpy as np
import ray
from const import *
from diff_equ import *

def solve_an(time_max:float, step:float, field = field, *args, **kwargs):
    '''
    Решение аналитической задачи\n
    Параметры:
    -
    time_max - максимальное время, до которого решается задача\n
    step - шаг сетки
    '''
    t_pred = 0
    t = step

    while t < time_max or (x1(t_pred, **kwargs) == 0 and x2(t_pred, **kwargs) == 0):
        if field(x1(t, **kwargs)) > x2(t, **kwargs):
            break
        else:
            t_pred = t
            t = t + step

    if t == time_max:
        raise ValueError(f'Не получилось найти решение до {time_max}')
    
    func = lambda t, **kwargs: - x2(t, **kwargs) + field(x1(t, **kwargs))
    
    t = sekush(func, t_pred, t, time_max, **kwargs)

    times = np.arange(0, t + step*3, step, dtype=np.float128)
    graph_x = np.array([x1(t, **kwargs) for t in times], dtype=np.float128)
    graph_y = np.array([x2(t, **kwargs) for t in times], dtype=np.float128)
    
     
    x = x1(t, **kwargs)
    y = x2(t, **kwargs)
    return x, y, t, graph_x, graph_y

def solve_runge(time_max:float, step:float, mode:bool, u:float, cos_a:float, sin_a:float, field=field, *args, **kwargs):
    '''
    Решает задачку движения по Рунге-Кутты\n
    Параметры:
    -
    time_max - максимальное время, до которого решается задача\n
    step - шаг сетки
    '''
    x = [0,0]
    y = [0,0]
    ux = [cos_a*u, cos_a*u]
    uy = [sin_a*u, sin_a*u]
    t = 0
    history_x = np.array(list(), dtype=np.float128)
    history_y = np.array(list(), dtype=np.float128)
    history_ux = np.array(list(), dtype=np.float128)
    history_uy = np.array(list(), dtype=np.float128)
    
    while(y[1] > field(x[1]) and t < time_max or (x[1] == 0 and y[1] == 0)):
        x[0], y[0], uy[0], ux[0] = x[1], y[1], uy[1], ux[1]
        history_x, history_y, history_uy, history_ux = np.append(history_x, x[0]), np.append(history_y, y[0]), np.append(history_uy, uy[0]), np.append(history_ux, ux[0])
        # x[1], y[1] = runge(x[1], t, step, ux), runge(y[1], t, step, uy)
        x[1], y[1], ux[1], uy[1] = runge_cord(t, history_ux[-4:], step, x1_usk, x[1], mode, **kwargs), runge_cord(t, history_uy[-4:], step, x2_usk, y[1], mode, **kwargs), runge_skor(t, history_ux[-4:], step, x1_usk, mode, **kwargs), runge_skor(t, history_uy[-4:], step, x2_usk, mode, **kwargs)
        t += step
    
    if t == time_max:
        raise ValueError(f'Не получилось решить по Рунге-Кутты за {time_max}')
    
    
    t-=step
    x_n = x[0]
    y_n = y[0]
    ux_n = np.array([ux[0]], dtype=np.float128)
    uy_n = np.array([uy[0]], dtype=np.float128)
    pred_step = step
    step /= 3
    x_slise = history_x[-1:]
    y_slize = history_y[-1:]
    for i in np.linspace(t, t+pred_step, 4, True)[1:-1]:
        x_n, y_n, ux_n_n, uy_n_n = runge_cord(i, ux_n, step, x1_usk, x_n,mode, **kwargs), runge_cord(i, uy_n, step, x2_usk, y_n, mode, **kwargs), runge_skor(i, ux_n, step, x1_usk, mode, **kwargs), runge_skor(i, uy_n, step, x2_usk, mode, **kwargs)
        ux_n, uy_n = np.append(ux_n, ux_n_n), np.append(uy_n, uy_n_n)
        x_slise, y_slize = np.append(x_slise, x_n), np.append(y_slize, y_n)
    history_x, history_y, history_uy, history_ux = np.append(history_x, x[1]), np.append(history_y, y[1]), np.append(history_uy, uy[1]), np.append(history_ux, ux[1])
    x_slise, y_slize = np.append(x_slise, x[1]), np.append(y_slize, y[1])
    cix = np.array([ci(x_slise, i) for i in x_slise], dtype=np.float128)

    func = lambda t, **kwargs: -y_x(t, **kwargs) + field(t)
    # a, b = x[0], x[1]
    # x1 = a
    
    kwargs.update([['yi', y_slize], ['xi',x_slise], ['cix', cix]])
    
    x_fin = sekush(func, x[0], x[1], time_max, **kwargs)
    y_fin = y_x(x_fin, y_slize, x_slise, cix)
    t_fin = y_x(x_fin, np.array([t, t + step, t + 2*step, t + pred_step], dtype=np.float128), x_slise, cix)
    return x_fin, y_fin, t_fin, history_x, history_y, history_ux, history_uy

@ray.remote
def solve_an_par(*arg, **kwargs):
    return solve_an(*arg, **kwargs)

@ray.remote
def solve_runge_par(*arg, **kwargs):
    return solve_runge(*arg, **kwargs)

if __name__ =='__main__':
    setting={
        'time_max': 1_000_000,
        'step':0.001,
        'cos_a':cos(45*np.pi/180),
        'sin_a':sin(45*np.pi/180),
        'm': 2,
        'u':17,
        'g':9.81,
        'field': lambda *args, **kwargs: 0,
        'a': 0
    }
    res = solve_an(**setting)
    print(res[2])
    print(setting['u']*setting['sin_a']*2/setting['g'])

