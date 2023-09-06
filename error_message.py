from PyQt6 import QtWidgets

def error_message(message:str):
    mes_box = QtWidgets.QMessageBox()
    mes_box.setText(str(message))
    mes_box.addButton(QtWidgets.QMessageBox.StandardButton.Ok)
    mes_box.addButton(QtWidgets.QMessageBox.StandardButton.Cancel)
    mes_box.exec()