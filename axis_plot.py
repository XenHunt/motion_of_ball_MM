import numpy as np
from numpy import pi, cos, sin
import ray

def axis_plot(time_max, step, func, *args, **kwargs):
    k = pi/180

    x_fin_array = np.array(list(), ndmin=1)
    y_fin_array = np.array(list(), ndmin=1)
    t_fin_array = np.array(list(), ndmin=1)

    alphas = np.arange(0, 361, 1, dtype=np.float128)*k
    cos_a = np.array([cos(i) for i in alphas], np.float128)
    sin_a = np.array([sin(i) for i in alphas], dtype=np.float128)
    
    operations = [func.remote(time_max, step, sin_a = sin_a[i], cos_a=cos_a[i], **kwargs) for i in range(len(cos_a))]
    results = ray.get(operations)
    
    x_fin_array = np.append(x_fin_array,[j[0] for j in results])
    y_fin_array = np.append(y_fin_array, [j[1] for j in results])
    t_fin_array = np.append(t_fin_array, [j[2] for j in results])
    
    return x_fin_array, y_fin_array, t_fin_array, alphas/k