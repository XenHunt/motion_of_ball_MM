import numpy as np
from numpy import sqrt
from solve import *
import ray
import matplotlib.pyplot as plt

def error_plot(time_max, steps, start, end, *args, **kwargs):
    steps = np.arange(start, end, steps, dtype = np.float128)
    
    lenght = np.arange(len(steps))
    
    operations_rung = [solve_runge.remote(time_max, i, **kwargs) for i in steps]
    operations_an = [solve_an.remote(time_max, i, **kwargs) for i in steps]
    
    results_rung = ray.get(operations_rung) # [number, what]
    results_an = ray.get(operations_an)
    
    times = [np.arange(0, results_an[i][2] + steps[i], steps[i], dtype=np.float128) for i in lenght] # [number, times]
    
    x1_an = [np.array([x1(t, **kwargs) for t in time], dtype=np.float128) for time in times] # [number, x1]
    x2_an = [np.array([x2(t, **kwargs) for t in time], dtype=np.float128) for time in times] # [number, x2]
    ux1_an = [np.array([ux1(t, **kwargs) for t in time], dtype=np.float128) for time in times] # [number, ux1]
    ux2_an = [np.array([ux2(t, **kwargs) for t in time], dtype=np.float128) for time in times] # [number, ux2]
    
    diff_ux1 = [ux1_an[i] - results_rung[i][5] for i in lenght] # [number, diff]
    diff_ux2 = [ux2_an[i] - results_rung[i][6] for i in lenght] # [number, diff]
    diff_x1 = [x1_an[i] - results_rung[i][3] for i in lenght] # [number, diff]
    diff_x2 = [x2_an[i] - results_rung[i][4] for i in lenght] # [numbder, diff]
    
    diff_x1 = [diff_x1[i] * diff_x1[i] for i in lenght] # [number, diff^2]
    diff_x2 = [diff_x2[i] * diff_x2[i] for i in lenght] # [number, diff^2]
    diff_ux1 = [diff_ux1[i] * diff_ux1[i] for i in lenght] # [number, diff^2]
    diff_ux2 = [diff_ux2[i] * diff_ux2[i] for i in lenght] # [number, diff^2]
    
    error = [sqrt( diff_x1[i] + diff_x2[i] + diff_ux1[i] + diff_ux2[i]) for i in lenght] # [number]
    errors = np.array([], np.float128)
    
    for i in lenght:
        errors = np.append(errors, np.max(error[i]))
    
    return steps, errors

def error(start, end, time_max, step,**kwargs):
    
    errors = np.array(list(), ndmin=1)
    for i in np.arange(start, end, step):
        time, _, _, _, _ =solve_an(time_max, i, **kwargs)
        times = np.arange(0, time + i, i, dtype=np.float128)
        x1_an = np.array([x1(t, **kwargs) for t in times], dtype=np.float128)
        x2_an = np.array([x2(t, **kwargs) for t in times], dtype=np.float128)
        ux1_an = np.array([ux1(t, **kwargs) for t  in times], dtype=np.float128)
        ux2_an = np.array([ux2(t, **kwargs) for t  in times], dtype=np.float128)   
        _, _, _, x1_rung, x2_rung, ux1_rung, ux2_rung = solve_runge(time_max, i, **kwargs)
        dif_ux = ux1_an[:ux1_rung.shape[0]] - ux1_rung[:ux1_an.shape[0]]
        dif_uy = ux2_an[:ux2_rung.shape[0]] - ux2_rung[:ux2_an.shape[0]]
        dif_x = x1_an[:x1_rung.shape[0]] - x1_rung[:x1_an.shape[0]]
        dif_y = x2_an[:x2_rung.shape[0]] - x2_rung[:x2_an.shape[0]]
        error_one = np.sqrt(dif_ux*dif_ux + dif_uy*dif_uy + dif_x*dif_x + dif_y*dif_y).max()/(i*i*i*i)
        print(error_one)
        errors = np.append(errors, error_one)

    return np.arange(start, end, step), errors