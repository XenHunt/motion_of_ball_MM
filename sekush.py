import numpy as np

def sekush(func, start:float, end:float, time_max:float, eps = 1e-7, *args, **kwargs)->float:
    '''
    Функция вычисялющая точку пересечения дфух графиков по методу секущих\n
    Параметры:
    -
    func - lambda функция разницы двух функций по типу lambda fi, x1, x2, t: fi(x1(t)) - x2(t)\n
    a и b - начало и конец отрезка пересечения\n
    time_max - максимальное кол-во итераций для поиска
    '''
    # x1 = a
    x = [start, end]
    for i in np.arange(time_max):
        if abs(x[0] - x[1]) < eps:
            return x[0]
        y0 = func(x[0], time_max=time_max, **kwargs)
        y1 = func(x[1], time_max=time_max, **kwargs)
        x3 = x[0] - (x[1] - x[0])*y0/(y1 - y0)
        x[0], x[1] = x[1], x3
        # y0 = func(field, x1_func, x2_func, a)
        # y1 = func(field, x1_func, x2_func, b)
        # x0 = b - (y1*(b - a))/(y1 - y0)
        # if y0 * func(field, x1_func, x2_func, x0) > 0:
        #     b = x0
        # else:
        #     a = x0
        # if abs(x1 - x0) < 1e-5:
        #     return x0
        # x1 = x0
    raise ValueError(f"Метод не сошелся за {time_max} итераций")

if __name__ == "__main__":
    setting = {
        "time_max": 1_000_000,
        'func': lambda t, **kwargs: t,
        'start': -10,
        'end': 10
    }
    print(sekush(**setting))