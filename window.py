from MainWindow import Ui_MainWindow as um
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
matplotlib.use('QtAgg')
from PyQt6 import QtWidgets
from solve_run import solve_all
from numpy import pi, cos, sin, sqrt
from axis_plot import axis_plot as ap
from solve import *
from error_plot import error as er
from error_message import *
from reverse_plot import reverse_plot as rp
import matplotlib.pyplot as plt

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QMainWindow, um):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.canvas = MplCanvas(self, width=10, height=10)
        
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        
        self.vertLay.addWidget(self.toolbar, 2)
        self.vertLay.addWidget(self.canvas, 8)
        self.buildPlot.clicked.connect(self.plot)
        self.buildAxisPlot.clicked.connect(self.plotAxis)
        self.keys = {'Аналитический способ':'an', 'Рунге-Кутты':'runge', 'Аддамс':'ad'}
        self.buildAxisPlot.clicked.connect(self.plotAxis)
        self.errorButton.clicked.connect(self.plotError)
        self.reverseButton.clicked.connect(self.plotReverse)
        self.massReverseButton.clicked.connect(self.manyPlotReverse)
        self.show()
        
    def plot(self):
        setting = {
            'time_max':1_000_000,
            'step': float(self.stepLine.text()),
            'cos_a': cos(float(self.axisLine.text())*pi/180),
            'sin_a': sin(float(self.axisLine.text())*pi/180),
            'u': sqrt(2*float(self.energyLine.text())/float(self.massLine.text())),
            'm': float(self.massLine.text()),
            'a': float(self.kLine.text()),
            'g': float(self.gLine.text()),
            'mode': self.keys[self.modeBox.currentText()]
        }
        
        x, y, t, xi, yi, fi = solve_all(**setting)
        
        self.canvas.axes.cla()
        self.canvas.axes.plot(xi, yi, label='Движение снаряда')
        self.canvas.axes.plot(xi, fi, label='Поверхность')
        self.canvas.axes.scatter(x, y, marker='x', s=30)
        self.canvas.axes.scatter(0, 0, marker='o', s = 40)
        self.canvas.axes.legend()
        self.canvas.axes.set_xlabel('X')
        self.canvas.axes.set_ylabel('Y')
        self.canvas.axes.set_title(f'Координата падения - ({x:.3f}, {y:.3f})\nВремя полёта - {t:.3f} с', y=-0.1)
        self.canvas.draw()
        
    def plotAxis(self):
        setting = {
            'time_max':1_000_000,
            'step': float(self.stepLine.text()),
            'u': sqrt(2*float(self.energyLine.text())/float(self.massLine.text())),
            'm': float(self.massLine.text()),
            'a': float(self.kLine.text()),
            'g': float(self.gLine.text()),
            'mode': self.keys[self.modeBox.currentText()]
        }
        
        m = setting['mode']
        
        if m == 'an':
            func = solve_an_par
        elif m == 'runge' or m == 'ad':
            func = solve_runge_par
            if m == 'runge':
                m = False
            else:
                m = True
        else:
            return
        
        setting['mode'] = m 
        setting['func'] = func
        
        x, y, t, axis = ap(**setting)
        
        
        
        self.canvas.axes.cla()
        self.canvas.axes.plot(axis, x, label='Координата X')
        self.canvas.axes.plot(axis, y, label='Координата Y')
        self.canvas.axes.plot(axis, t, label='Время полёта')
        self.canvas.axes.set_xlabel('')
        self.canvas.axes.set_ylabel('')
        self.canvas.axes.legend()
        self.canvas.draw()
        
    
    def plotReverse(self):
        setting = {
            'time_max':1_000,
            'step': float(self.stepLine.text()),
            'u': sqrt(2*float(self.energyLine.text())/float(self.massLine.text())),
            'm': float(self.massLine.text()),
            'a': float(self.kLine.text()),
            'g': float(self.gLine.text()),
            'mode': self.keys[self.modeBox.currentText()]
        }
        
        if setting['mode'] == 'an':
            setting['function'] = solve_an_par
            setting['par_function'] = solve_an_par
        else:
            setting['function'] = solve_runge_par
            setting['par_function'] = solve_runge_par
            if setting['mode'] == 'ad':
                setting['mode']= True
            else:
                setting['mode'] = False
        
        self.canvas.axes.cla()
        x_arr = np.arange(float(self.fromLine.text()), 
                          float(self.toLine.text()),
                          setting['step'], dtype=np.float128)
        self.canvas.axes.plot(x_arr, [field(i) for i in x_arr], label='Поверхность')
        self.canvas.draw()
        
        clicked = []
        
        def event_click(event):
            clicked.append(event.xdata)
            clicked.append(event.ydata)
            self.canvas.mpl_disconnect(cid)
            setting['field'] = lambda t: max(t*clicked[1]/clicked[0], field(t))
            try:
                result = rp(clicked[0], clicked[1], **setting)
                if result[0] == None:
                    raise ValueError('Не получается достичь это числа')
                alpha = result[0]
                setting['cos_a'] = cos(alpha)
                setting['sin_a'] = sin(alpha)
                setting['mode'] = self.keys[self.modeBox.currentText()]
                setting['field'] = field
                _, _, _, xi, yi, _ = solve_all(**setting)
            
                self.canvas.axes.plot(xi, yi, label='Движение снаряда')
                self.canvas.axes.scatter(0, 0, marker='o', s = 40)
                self.canvas.axes.scatter(clicked[0], clicked[1], marker='h', s=40)
                self.canvas.axes.legend()
                self.canvas.axes.set_xlabel('X')
                self.canvas.axes.set_ylabel('Y')
                self.canvas.axes.set_title(f'Угол - {alpha*180/pi:.2f}', y=-0.1)
                self.canvas.draw()
            except Exception as e:
                error_message(e)
            
        error_message('Кликните там, где будете искать угол падения')
        cid = self.canvas.mpl_connect('button_press_event', event_click)
        
    
    def plotError(self):
        setting = {
            'time_max':1_000_000,
            'step': float(self.stepLine.text()),
            'cos_a': cos(float(self.axisLine.text())*pi/180),
            'sin_a': sin(float(self.axisLine.text())*pi/180),
            'u': sqrt(2*float(self.energyLine.text())/float(self.massLine.text())),
            'm': float(self.massLine.text()),
            'a': float(self.kLine.text()),
            'g': float(self.gLine.text()),
            'mode': self.keys[self.modeBox.currentText()],
            'start': float(self.startLineEdit.text()),
            'end': float(self.endLineEdit.text())
        }
        
        if setting['mode'] == 'ad':
            setting['mode'] = True
        else:
            setting['mode'] = False
           
        st, error = er(**setting)
        
        self.canvas.axes.cla()
        self.canvas.axes.plot(st, error, label='Ошибка на шаг в 4-ой степени')
        self.canvas.axes.set_xlabel('Шаг')
        self.canvas.axes.set_ylabel('Ошибка')
        self.canvas.axes.semilogx()
        self.canvas.axes.legend()
        self.canvas.draw()
       
    def manyPlotReverse(self):
        setting = {
            'time_max':1_000,
            'step': float(self.stepLine.text()),
            'u': sqrt(2*float(self.energyLine.text())/float(self.massLine.text())),
            'm': float(self.massLine.text()),
            'a': float(self.kLine.text()),
            'g': float(self.gLine.text()),
            'mode': self.keys[self.modeBox.currentText()],
            'number': int(self.massReverseLine.text())
        }
        
        if setting['mode'] == 'an':
            setting['function'] = solve_an_par
            setting['par_function'] = solve_an_par
        else:
            setting['function'] = solve_runge_par
            setting['par_function'] = solve_runge_par
            if setting['mode'] == 'ad':
                setting['mode']= True
            else:
                setting['mode'] = False
        
        self.canvas.axes.cla()
        x_arr = np.arange(float(self.fromLine.text()), 
                          float(self.toLine.text()),
                          setting['step'], dtype=np.float128)
        self.canvas.axes.plot(x_arr, [field(i) for i in x_arr], label='Поверхность')
        self.canvas.draw()
        
        clicked = []
        
        def event_click(event):
            clicked.append([event.xdata, event.ydata])
            if (len(clicked) >= setting['number']):
                self.canvas.mpl_disconnect(cid)
                for click in clicked:
                    self.canvas.axes.scatter(click[0], click[1], s=30, marker='h')
                numbers = self.plotMass(clicked, field, **setting)
                error_message(f'Было построенно - {numbers[0]} точек\nНе получилось построить - {numbers[1]} точки')
            
            
            
        error_message(f'Кликните {setting["number"]} точки')
        cid = self.canvas.mpl_connect('button_press_event', event_click) 
            
    def plotMass(self, clicked, true_field, **setting):
        number_suc = 0
        number_fail = 0
        alphas = []
        for i, click in enumerate(clicked):
            try:
                alphas.append(ray.get(rp.remote(click[0], click[1], field = lambda t: max(t*click[1]/click[0], true_field(t)), **setting))[0])
                number_suc += 1
            except Exception as e:
                number_fail += 1
                print(str(e))
        # operations = [rp.remote(click[0], click[1], field = lambda t: max(t*click[1]/click[0], true_field(t)), **setting) for click in clicked]
        # alphas = np.array([ray.get(op)[0] for op in operations], dtype=np.float128)
        # delete_alphas = []
        # for i in range(len(alphas)):
        #     if i == None:
        #         number_fail +=1
        #         delete_alphas.append(i)
        #     else:
        #         number_suc+=1
        
        # alphas = np.delete(alphas, delete_alphas)
        
        setting['mode'] = self.keys[self.modeBox.currentText()]
        setting['field'] = field
        
        operations = [setting['function'].remote(sin_a = sin(i), cos_a = cos(i), **setting) for i in alphas]
        results = ray.get(operations)
        
        for res in results:
            self.canvas.axes.plot(res[3], res[4])
        
        self.canvas.axes.set_xlabel('X')
        self.canvas.axes.set_ylabel('Y')
        self.canvas.draw()
        
        return number_suc, number_fail