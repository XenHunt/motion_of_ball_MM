from window import MainWindow as mw
from PyQt6 import QtWidgets
import ray
import sys

ray.init()

app = QtWidgets.QApplication(sys.argv)
window = mw()
app.exec()