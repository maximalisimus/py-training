

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        w = AnotherWindow()
        w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()


------------------------------------------------------------------------

import sys
from PyQt5.Qt import *


class Window_2(QMainWindow):                             # !!! QMainWindow
    def __init__(self, parent=None):
        super().__init__(parent)                         # !!! parent
        self.setWindowTitle("Window_2")
        self.resize(200, 215)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Lab 2-3")
        self.setGeometry(590, 300, 480, 215)
        self.setStyleSheet("background : white;")
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
  
        self.button = QPushButton('Создать второе окно')
        self.button.clicked.connect(self.create_window) 
        
        self.grid_layout = QGridLayout(self.centralWidget)
        self.grid_layout.addWidget(self.button)
        
    def create_window(self):
        self.window = Window_2(self)                        # !!! self
        self.window.show()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

------------------------------------------------------------------------

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = AnotherWindow()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

------------------------------------------------------------------------

Showing & hiding persistent windows

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint


class AnotherWindow(QWidget):
	"""
	This "window" is a QWidget. If it has no parent, it
	will appear as a free-floating window as we want.
	"""
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()
		self.label = QLabel("Another Window % d" % randint(0,100))
		layout.addWidget(self.label)
		self.setLayout(layout)


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.w = AnotherWindow()
		self.button = QPushButton("Push for Window")
		self.button.clicked.connect(self.toggle_window)
		self.setCentralWidget(self.button)

	def toggle_window(self, checked):
		if self.w.isVisible():
			self.w.hide()

		else:
			self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()





















