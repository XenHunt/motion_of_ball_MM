from sekush import sekush
from numpy import sqrt, cos, sin, pi
from error_message import error_message as em
import ray
from const import field
from solve import solve_runge
from axis_plot import axis_plot as ap
import numpy as np

def reverse_plot(x1, x2, **kwargs):
    def range_solve(alpha, function, **kwargs):
        kwargs['cos_a'] = cos(alpha)
        kwargs['sin_a'] = sin(alpha)
        r = ray.get(function.remote(**kwargs))
        diff_1 =x1 - r[0]
        # print(diff_1)
        return diff_1

    f = lambda alpha, **kwargs: range_solve(alpha, **kwargs)
    axis_p = ap(func=kwargs['function'], **kwargs)
    max_cord = np.argmax(axis_p[0])
    min_cord = np.argmin(axis_p[0])
    try:
        alpha = sekush(f, min_cord*np.pi/180, max_cord*np.pi/180, **kwargs)
    except Exception as e:
        raise ValueError('Не получается достичь этой точки по методу секущих')
    kwargs['cos_a'] = cos(alpha)
    kwargs['sin_a'] = sin(alpha)
    r = ray.get(kwargs['function'].remote(**kwargs))
    if abs(r[0] - x1) >= 1e-2 or abs(r[1] - x2) >= 1e-2:
        return None, None, None
    return alpha, r[0], r[1]

if __name__ == '__main__':
    ray.init()
    cord = 13.2
    setting = {
        'time_max':1_000_000,
        'step': 0.001,
        'u': sqrt(2*300/2),
        'm': 2,
        'a': 0.5,
        'g': 9.81,
        'mode': True,
        'function': solve_runge,
    }
    alpha = ray.get(reverse_plot.remote(cord, field(cord), **setting))[0] # Должно быть 45
    setting['cos_a'] = cos(alpha)
    setting['sin_a'] = sin(alpha)
    res = ray.get(solve_runge.remote(**setting))
    print(res[0])
    print(res[1])
    print(field(13.2))
    