import sys
from PyQt4 import QtGui, QtCore
from PyQt4 import QtCore, QtGui


class MainWidget(QtGui.QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setReadOnly(True)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.textEdit)

        self.setLayout(hbox)
