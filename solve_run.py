import numpy as np
from solve import *
from const import x1, x2, ux1, ux2, field
import ray
   
def solve_all(time_max, step, mode, *args, **kwargs):
    if mode == 'an':
        x, y, time, hist_x, hist_y = solve_an(time_max, step, **kwargs)

        times = np.arange(0, time + step*3, step, dtype=np.float128)
        graph_field = np.array([field(x) for x in hist_x], dtype=np.float128)
        
        return x, y, time, hist_x, hist_y, graph_field
        
    elif mode == 'runge' or mode =='ad':
        if mode == 'runge':
            mode = False
        elif mode == 'ad':
            mode = True
        
        x, y, t, hist_x, hist_y, _, _ = solve_runge(time_max, step, mode, **kwargs)
        field_hist = np.array([field(i) for i in hist_x], dtype=np.float128)
        
        return x, y, t, hist_x, hist_y, field_hist