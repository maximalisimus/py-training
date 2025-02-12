#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# pip install pyqt5 pyqt5-tools
#
# pyuic5 --version
## (env): env/pyqt-env/Lib/site-packages/qt5_applications/Qt/bin/
## assistant.exe
## designer.exe
## linguist.exe
## qml.exe
## ...
# pyuic5 -o ./forms/question_form.py ./forms/question_form.ui
# pyuic5 -o ./forms/settings_form.py ./forms/settings_form.ui
# pyrcc5 -o ./forms/resources.py ./forms/resources.qrc
# 

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QAction, QMenu, QFileDialog
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QKeySequence

qt_resource_data = b"\
\x00\x00\x04\xae\
\x3c\
\x3f\x78\x6d\x6c\x20\x76\x65\x72\x73\x69\x6f\x6e\x3d\x22\x31\x2e\
\x30\x22\x20\x65\x6e\x63\x6f\x64\x69\x6e\x67\x3d\x22\x75\x74\x66\
\x2d\x38\x22\x3f\x3e\x3c\x21\x2d\x2d\x20\x55\x70\x6c\x6f\x61\x64\
\x65\x64\x20\x74\x6f\x3a\x20\x53\x56\x47\x20\x52\x65\x70\x6f\x2c\
\x20\x77\x77\x77\x2e\x73\x76\x67\x72\x65\x70\x6f\x2e\x63\x6f\x6d\
\x2c\x20\x47\x65\x6e\x65\x72\x61\x74\x6f\x72\x3a\x20\x53\x56\x47\
\x20\x52\x65\x70\x6f\x20\x4d\x69\x78\x65\x72\x20\x54\x6f\x6f\x6c\
\x73\x20\x2d\x2d\x3e\x0a\x3c\x73\x76\x67\x20\x77\x69\x64\x74\x68\
\x3d\x22\x38\x30\x30\x70\x78\x22\x20\x68\x65\x69\x67\x68\x74\x3d\
\x22\x38\x30\x30\x70\x78\x22\x20\x76\x69\x65\x77\x42\x6f\x78\x3d\
\x22\x30\x20\x30\x20\x33\x32\x20\x33\x32\x22\x20\x78\x6d\x6c\x6e\
\x73\x3d\x22\x68\x74\x74\x70\x3a\x2f\x2f\x77\x77\x77\x2e\x77\x33\
\x2e\x6f\x72\x67\x2f\x32\x30\x30\x30\x2f\x73\x76\x67\x22\x3e\x3c\
\x74\x69\x74\x6c\x65\x3e\x66\x69\x6c\x65\x5f\x74\x79\x70\x65\x5f\
\x65\x78\x63\x65\x6c\x32\x3c\x2f\x74\x69\x74\x6c\x65\x3e\x3c\x70\
\x61\x74\x68\x20\x64\x3d\x22\x4d\x32\x38\x2e\x37\x38\x31\x2c\x34\
\x2e\x34\x30\x35\x48\x31\x38\x2e\x36\x35\x31\x56\x32\x2e\x30\x31\
\x38\x4c\x32\x2c\x34\x2e\x35\x38\x38\x56\x32\x37\x2e\x31\x31\x35\
\x6c\x31\x36\x2e\x36\x35\x31\x2c\x32\x2e\x38\x36\x38\x56\x32\x36\
\x2e\x34\x34\x35\x48\x32\x38\x2e\x37\x38\x31\x41\x31\x2e\x31\x36\
\x32\x2c\x31\x2e\x31\x36\x32\x2c\x30\x2c\x30\x2c\x30\x2c\x33\x30\
\x2c\x32\x35\x2e\x33\x34\x39\x56\x35\x2e\x35\x41\x31\x2e\x31\x36\
\x32\x2c\x31\x2e\x31\x36\x32\x2c\x30\x2c\x30\x2c\x30\x2c\x32\x38\
\x2e\x37\x38\x31\x2c\x34\x2e\x34\x30\x35\x5a\x6d\x2e\x31\x36\x2c\
\x32\x31\x2e\x31\x32\x36\x48\x31\x38\x2e\x36\x31\x37\x4c\x31\x38\
\x2e\x36\x2c\x32\x33\x2e\x36\x34\x32\x68\x32\x2e\x34\x38\x37\x76\
\x2d\x32\x2e\x32\x48\x31\x38\x2e\x35\x38\x31\x6c\x2d\x2e\x30\x31\
\x32\x2d\x31\x2e\x33\x68\x32\x2e\x35\x31\x38\x76\x2d\x32\x2e\x32\
\x48\x31\x38\x2e\x35\x35\x6c\x2d\x2e\x30\x31\x32\x2d\x31\x2e\x33\
\x68\x32\x2e\x35\x34\x39\x76\x2d\x32\x2e\x32\x48\x31\x38\x2e\x35\
\x33\x76\x2d\x31\x2e\x33\x68\x32\x2e\x35\x35\x37\x76\x2d\x32\x2e\
\x32\x48\x31\x38\x2e\x35\x33\x76\x2d\x31\x2e\x33\x68\x32\x2e\x35\
\x35\x37\x76\x2d\x32\x2e\x32\x48\x31\x38\x2e\x35\x33\x76\x2d\x32\
\x48\x32\x38\x2e\x39\x34\x31\x5a\x22\x20\x73\x74\x79\x6c\x65\x3d\
\x22\x66\x69\x6c\x6c\x3a\x23\x32\x30\x37\x34\x34\x61\x3b\x66\x69\
\x6c\x6c\x2d\x72\x75\x6c\x65\x3a\x65\x76\x65\x6e\x6f\x64\x64\x22\
\x2f\x3e\x3c\x72\x65\x63\x74\x20\x78\x3d\x22\x32\x32\x2e\x34\x38\
\x37\x22\x20\x79\x3d\x22\x37\x2e\x34\x33\x39\x22\x20\x77\x69\x64\
\x74\x68\x3d\x22\x34\x2e\x33\x32\x33\x22\x20\x68\x65\x69\x67\x68\
\x74\x3d\x22\x32\x2e\x32\x22\x20\x73\x74\x79\x6c\x65\x3d\x22\x66\
\x69\x6c\x6c\x3a\x23\x32\x30\x37\x34\x34\x61\x22\x2f\x3e\x3c\x72\
\x65\x63\x74\x20\x78\x3d\x22\x32\x32\x2e\x34\x38\x37\x22\x20\x79\
\x3d\x22\x31\x30\x2e\x39\x34\x22\x20\x77\x69\x64\x74\x68\x3d\x22\
\x34\x2e\x33\x32\x33\x22\x20\x68\x65\x69\x67\x68\x74\x3d\x22\x32\
\x2e\x32\x22\x20\x73\x74\x79\x6c\x65\x3d\x22\x66\x69\x6c\x6c\x3a\
\x23\x32\x30\x37\x34\x34\x61\x22\x2f\x3e\x3c\x72\x65\x63\x74\x20\
\x78\x3d\x22\x32\x32\x2e\x34\x38\x37\x22\x20\x79\x3d\x22\x31\x34\
\x2e\x34\x34\x31\x22\x20\x77\x69\x64\x74\x68\x3d\x22\x34\x2e\x33\
\x32\x33\x22\x20\x68\x65\x69\x67\x68\x74\x3d\x22\x32\x2e\x32\x22\
\x20\x73\x74\x79\x6c\x65\x3d\x22\x66\x69\x6c\x6c\x3a\x23\x32\x30\
\x37\x34\x34\x61\x22\x2f\x3e\x3c\x72\x65\x63\x74\x20\x78\x3d\x22\
\x32\x32\x2e\x34\x38\x37\x22\x20\x79\x3d\x22\x31\x37\x2e\x39\x34\
\x32\x22\x20\x77\x69\x64\x74\x68\x3d\x22\x34\x2e\x33\x32\x33\x22\
\x20\x68\x65\x69\x67\x68\x74\x3d\x22\x32\x2e\x32\x22\x20\x73\x74\
\x79\x6c\x65\x3d\x22\x66\x69\x6c\x6c\x3a\x23\x32\x30\x37\x34\x34\
\x61\x22\x2f\x3e\x3c\x72\x65\x63\x74\x20\x78\x3d\x22\x32\x32\x2e\
\x34\x38\x37\x22\x20\x79\x3d\x22\x32\x31\x2e\x34\x34\x33\x22\x20\
\x77\x69\x64\x74\x68\x3d\x22\x34\x2e\x33\x32\x33\x22\x20\x68\x65\
\x69\x67\x68\x74\x3d\x22\x32\x2e\x32\x22\x20\x73\x74\x79\x6c\x65\
\x3d\x22\x66\x69\x6c\x6c\x3a\x23\x32\x30\x37\x34\x34\x61\x22\x2f\
\x3e\x3c\x70\x6f\x6c\x79\x67\x6f\x6e\x20\x70\x6f\x69\x6e\x74\x73\
\x3d\x22\x36\x2e\x33\x34\x37\x20\x31\x30\x2e\x36\x37\x33\x20\x38\
\x2e\x34\x39\x33\x20\x31\x30\x2e\x35\x35\x20\x39\x2e\x38\x34\x32\
\x20\x31\x34\x2e\x32\x35\x39\x20\x31\x31\x2e\x34\x33\x36\x20\x31\
\x30\x2e\x33\x39\x37\x20\x31\x33\x2e\x35\x38\x32\x20\x31\x30\x2e\
\x32\x37\x34\x20\x31\x30\x2e\x39\x37\x36\x20\x31\x35\x2e\x35\x34\
\x20\x31\x33\x2e\x35\x38\x32\x20\x32\x30\x2e\x38\x31\x39\x20\x31\
\x31\x2e\x33\x31\x33\x20\x32\x30\x2e\x36\x36\x36\x20\x39\x2e\x37\
\x38\x31\x20\x31\x36\x2e\x36\x34\x32\x20\x38\x2e\x32\x34\x38\x20\
\x32\x30\x2e\x35\x31\x33\x20\x36\x2e\x31\x36\x33\x20\x32\x30\x2e\
\x33\x32\x39\x20\x38\x2e\x35\x38\x35\x20\x31\x35\x2e\x36\x36\x36\
\x20\x36\x2e\x33\x34\x37\x20\x31\x30\x2e\x36\x37\x33\x22\x20\x73\
\x74\x79\x6c\x65\x3d\x22\x66\x69\x6c\x6c\x3a\x23\x66\x66\x66\x66\
\x66\x66\x3b\x66\x69\x6c\x6c\x2d\x72\x75\x6c\x65\x3a\x65\x76\x65\
\x6e\x6f\x64\x64\x22\x2f\x3e\x3c\x2f\x73\x76\x67\x3e\
"

qt_resource_name = b"\
\x00\x08\
\x0a\x64\x65\x23\
\x00\x69\
\x00\x63\x00\x6f\x00\x6e\x00\x5f\x00\x72\x00\x65\x00\x73\
\x00\x09\
\x09\xbf\x83\x07\
\x00\x65\
\x00\x78\x00\x63\x00\x65\x00\x6c\x00\x2e\x00\x73\x00\x76\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x16\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x16\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x8e\xc2\xe4\x4e\x70\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
	rcc_version = 1
	qt_resource_struct = qt_resource_struct_v1
else:
	rcc_version = 2
	qt_resource_struct = qt_resource_struct_v2

def qInitResources():
	QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
	QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()

class ui_form(object):
	
	def __init__(self, form_obj, form_name):
		super().__init__()
		self.translate = QtCore.QCoreApplication.translate
		self.form_name = form_name
		self.form_obj = form_obj
	
	def set_geometry(self, left: int, top: int, width: int, height: int):
		self.form_obj.setGeometry(left, top, width, height)

	def set_size(self, width: int, height: int):
		self.form_obj.resize(width, height)

	def set_title(self, title: str):
		self.form_obj.setWindowTitle(self.translate(self.form_name, f"{title}"))

class DefaultWidget(QWidget):
	
	def __init__(self):
		super().__init__()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

class ui_question_form(ui_form):
	
	def setupUi(self, icon_settings: dict):
		self.form_obj.setObjectName(self.form_name)
		self.form_obj.resize(480, 96)
		self.form_obj.setMinimumSize(QtCore.QSize(128, 80))
		self.form_obj.setBaseSize(QtCore.QSize(128, 80))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(12)
		self.form_obj.setFont(font)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(icon_settings['forms']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.form_obj.setWindowIcon(icon)
		self.verticalLayout = QtWidgets.QVBoxLayout(self.form_obj)
		self.verticalLayout.setObjectName("verticalLayout")
		self.text_label = QtWidgets.QLabel(self.form_obj)
		self.text_label.setAlignment(QtCore.Qt.AlignCenter)
		self.text_label.setObjectName("text_label")
		self.text_label.setWordWrap(True)
		self.text_label.adjustSize()
		self.verticalLayout.addWidget(self.text_label)
		self.horizontal_widget = QtWidgets.QHBoxLayout()
		self.horizontal_widget.setObjectName("horizontal_widget")
		self.button_ok = QtWidgets.QPushButton(self.form_obj)
		self.button_ok.setObjectName("button_ok")
		self.horizontal_widget.addWidget(self.button_ok)
		self.button_no = QtWidgets.QPushButton(self.form_obj)
		self.button_no.setObjectName("button_no")
		self.horizontal_widget.addWidget(self.button_no)
		self.verticalLayout.addLayout(self.horizontal_widget)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self.form_obj)
	
	def set_text(self, text: str):
		self.text_label.setText(self.translate(self.form_name, f"{text}"))

	def set_ok_text(self, text_ok: str):
		self.button_ok.setText(self.translate(self.form_name, f"{text_ok}"))
		
	def set_no_text(self, text_no: str):
		self.button_no.setText(self.translate(self.form_name, f"{text_no}"))
	
	def retranslateUi(self):
		self.form_obj.setWindowTitle(self.translate(self.form_name, "Question"))
		self.text_label.setText(self.translate(self.form_name, "The text of question!"))
		self.button_no.setText(self.translate(self.form_name, "NO"))
		self.button_ok.setText(self.translate(self.form_name, "OK"))

class ui_settings_form(ui_form):
	def setupUi(self, icon_settings: dict):
		self.form_obj.setObjectName(self.form_name)
		self.form_obj.resize(600, 480)
		self.form_obj.setMinimumSize(QtCore.QSize(600, 480))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(12)
		self.form_obj.setFont(font)
		self.form_obj.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(icon_settings['forms']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.form_obj.setWindowIcon(icon)
		self.verticalLayout = QtWidgets.QVBoxLayout(self.form_obj)
		self.verticalLayout.setObjectName("verticalLayout")
		self.tab_widget = QtWidgets.QTabWidget(self.form_obj)
		self.tab_widget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.tab_widget.setStyleSheet("background-color: rgb(240, 240, 240);")
		self.tab_widget.setTabPosition(QtWidgets.QTabWidget.West)
		self.tab_widget.setObjectName("tab_widget")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.gridLayout = QtWidgets.QGridLayout(self.tab)
		self.gridLayout.setObjectName("gridLayout")
		self.label_regular = QtWidgets.QLabel(self.tab)
		self.label_regular.setStyleSheet("padding: 5px;")
		self.label_regular.setObjectName("label_regular")
		self.gridLayout.addWidget(self.label_regular, 1, 0, 1, 1)
		self.edit_regular = QtWidgets.QLineEdit(self.tab)
		self.edit_regular.setStyleSheet("background-color: rgb(255, 255, 255);\npadding: 5px;")
		self.edit_regular.setObjectName("edit_regular")
		self.gridLayout.addWidget(self.edit_regular, 1, 1, 1, 1)
		self.label_zip = QtWidgets.QLabel(self.tab)
		self.label_zip.setStyleSheet("padding: 5px;")
		self.label_zip.setObjectName("label_zip")
		self.gridLayout.addWidget(self.label_zip, 2, 0, 1, 1)
		self.edit_zip = QtWidgets.QLineEdit(self.tab)
		self.edit_zip.setStyleSheet("background-color: rgb(255, 255, 255);\npadding: 5px;")
		self.edit_zip.setObjectName("edit_zip")
		self.gridLayout.addWidget(self.edit_zip, 2, 1, 1, 1)
		self.edit_info = QtWidgets.QTextEdit(self.tab)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.edit_info.sizePolicy().hasHeightForWidth())
		self.edit_info.setSizePolicy(sizePolicy)
		self.edit_info.setStyleSheet("background-color: rgb(240, 240, 240);")
		self.edit_info.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.edit_info.setFrameShadow(QtWidgets.QFrame.Plain)
		self.edit_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
		self.edit_info.setUndoRedoEnabled(False)
		self.edit_info.setAcceptRichText(False)
		self.edit_info.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
		self.edit_info.setObjectName("edit_info")
		self.gridLayout.addWidget(self.edit_info, 3, 0, 1, 2)
		self.label_html = QtWidgets.QLabel(self.tab)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_html.sizePolicy().hasHeightForWidth())
		self.label_html.setSizePolicy(sizePolicy)
		self.label_html.setStyleSheet("padding: 5px;")
		self.label_html.setAlignment(QtCore.Qt.AlignCenter)
		self.label_html.setObjectName("label_html")
		self.gridLayout.addWidget(self.label_html, 0, 0, 1, 2)
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(icon_settings['html']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.tab_widget.addTab(self.tab, icon1, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.label_zipconfig = QtWidgets.QLabel(self.tab_2)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_zipconfig.sizePolicy().hasHeightForWidth())
		self.label_zipconfig.setSizePolicy(sizePolicy)
		self.label_zipconfig.setStyleSheet("padding: 5px;")
		self.label_zipconfig.setAlignment(QtCore.Qt.AlignCenter)
		self.label_zipconfig.setObjectName("label_zipconfig")
		self.gridLayout_2.addWidget(self.label_zipconfig, 0, 0, 1, 1)
		self.check_run = QtWidgets.QCheckBox(self.tab_2)
		self.check_run.setStyleSheet("padding: 5px;")
		self.check_run.setChecked(True)
		self.check_run.setObjectName("check_run")
		self.gridLayout_2.addWidget(self.check_run, 1, 0, 1, 1)
		self.check_zip = QtWidgets.QCheckBox(self.tab_2)
		self.check_zip.setStyleSheet("padding: 5px;")
		self.check_zip.setObjectName("check_zip")
		self.gridLayout_2.addWidget(self.check_zip, 2, 0, 1, 1)
		spacerItem = QtWidgets.QSpacerItem(532, 330, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(icon_settings['zip']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.tab_widget.addTab(self.tab_2, icon2, "")
		self.verticalLayout.addWidget(self.tab_widget)
		self.horizontal_layout = QtWidgets.QHBoxLayout()
		self.horizontal_layout.setObjectName("horizontal_layout")
		self.upload_btn = QtWidgets.QPushButton(self.form_obj)
		self.upload_btn.setStyleSheet("padding: 5px;")
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(icon_settings['refresh']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.upload_btn.setIcon(icon3)
		self.upload_btn.setObjectName("upload_btn")
		self.horizontal_layout.addWidget(self.upload_btn)
		self.clear_btn = QtWidgets.QPushButton(self.form_obj)
		self.clear_btn.setStyleSheet("padding: 5px;")
		icon4 = QtGui.QIcon()
		icon4.addPixmap(QtGui.QPixmap(icon_settings['clear']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.clear_btn.setIcon(icon4)
		self.clear_btn.setObjectName("clear_btn")
		self.horizontal_layout.addWidget(self.clear_btn)
		self.save_btn = QtWidgets.QPushButton(self.form_obj)
		self.save_btn.setStyleSheet("padding: 5px;")
		icon5 = QtGui.QIcon()
		icon5.addPixmap(QtGui.QPixmap(icon_settings['save']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.save_btn.setIcon(icon5)
		self.save_btn.setObjectName("save_btn")
		self.horizontal_layout.addWidget(self.save_btn)
		self.uses_btn = QtWidgets.QPushButton(self.form_obj)
		self.uses_btn.setStyleSheet("padding: 5px;")
		icon6 = QtGui.QIcon()
		icon6.addPixmap(QtGui.QPixmap(icon_settings['uses']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.uses_btn.setIcon(icon6)
		self.uses_btn.setObjectName("uses_btn")
		self.horizontal_layout.addWidget(self.uses_btn)
		self.verticalLayout.addLayout(self.horizontal_layout)

		self.retranslateUi()
		self.tab_widget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(self.form_obj)

	def get_edit_reg(self):
		return self.edit_regular.text()

	def set_edit_reg(self, value: str):
		self.edit_regular.setText(self.translate(self.form_name, f"{value}"))

	def get_edit_zip(self):
		return self.edit_zip.text()

	def set_edit_zip(self, value: str):
		self.edit_zip.setText(self.translate(self.form_name, f"{value}"))

	def get_check_run(self):
		return self.check_run.isChecked()

	def set_check_run(self, value: bool):
		self.check_run.setChecked(value)

	def get_check_zip(self):
		self.check_zip.isChecked()

	def set_check_zip(self, value: bool):
		self.check_zip.setChecked(value)
	
	'''
	def text_info_copy():
		self.edit_info.copy()
	'''

	def retranslateUi(self):
		self.form_obj.setWindowTitle(self.translate(self.form_name, "Настройки"))
		self.label_regular.setText(self.translate(self.form_name, "<html><head/><body><p><span style=\" font-weight:600;\">Наименование отчета:</span></p></body></html>"))
		self.edit_regular.setText(self.translate(self.form_name, "REPORT_START-STOP_RYEARS"))
		self.label_zip.setText(self.translate(self.form_name, "<html><head/><body><p><span style=\" font-weight:600;\">Наименование папки с архивом:</span></p></body></html>"))
		self.edit_zip.setText(self.translate(self.form_name, "Архив_START-STOP_RYEARS"))
		self.edit_info.setHtml(self.translate(self.form_name, "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt;\">В данных строках настроек используютя регулярные выражения</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt;\">для замены конкретного текста на предустановленный.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt;\">Для настройки имён отчётов вы можете использовать следующие имена</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt;\">регулярных выражений.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt;\">Данные замены являются фиксированными </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt;\">и никак не могут быть изменены.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600;\">REPORT</span><span style=\" font-family:\'Arial\'; font-size:12pt;\"> - заменяется на &quot;Сводная-таблица&quot;.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600;\">START</span><span style=\" font-family:\'Arial\'; font-size:12pt;\"> - Начальный месяц отчёта.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600;\">STOP</span><span style=\" font-family:\'Arial\'; font-size:12pt;\"> - Конечный месяц отчёта.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600;\">CDAY</span><span style=\" font-family:\'Arial\'; font-size:12pt;\"> - Дата текущего дня, только одного дня.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600;\">CMONTH</span><span style=\" font-family:\'Arial\'; font-size:12pt;\"> - Дата текущего месяца, только одного месяца.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600;\">CYEARS</span><span style=\" font-family:\'Arial\'; font-size:12pt;\"> - Дата текущего года, только одного года.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600;\">CDATE</span><span style=\" font-family:\'Arial\'; font-size:12pt;\"> - Полная текущая дата в формате &quot;день.месяц.год&quot;, например 01.01.2024.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600;\">RYEARS</span><span style=\" font-family:\'Arial\'; font-size:12pt;\"> - Год, полученный из настроек excel файла.</span></p></body></html>"))
		self.label_html.setText(self.translate(self.form_name, "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Настройки отчётности.</span></p></body></html>"))
		self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab), self.translate(self.form_name, "html"))
		self.label_zipconfig.setText(self.translate(self.form_name, "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Настройки архивов.</span></p></body></html>"))
		self.check_run.setText(self.translate(self.form_name, "Открыть отчёт после создания"))
		self.check_zip.setText(self.translate(self.form_name, "Открыть папку с архивом после формирования"))
		self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_2), self.translate("settings_form", "Архивы"))
		self.upload_btn.setText(self.translate(self.form_name, "Перезагрузить"))
		self.clear_btn.setText(self.translate(self.form_name, "Сбросить"))
		self.save_btn.setText(self.translate(self.form_name, "Сохранить"))
		self.uses_btn.setText(self.translate(self.form_name, "Применить"))

class SettingsForm(DefaultWidget):
	
	def __init__(self, icon_settings: dict, title: str = "Settings"):
		super().__init__()
		self.ui = ui_settings_form(self, "settings_form")
		self.ui.setupUi(icon_settings)
		self.ui.set_title(title)
		self.center()
		self.show()

class QuestionForm(DefaultWidget):
	
	def __init__(self, icon_settings: dict, title: str = "Question", text: str = "The text of question!", ok_text: str = "OK", no_text: str = "CANCEL"):
		super().__init__()
		self.ui = ui_question_form(self, "question_form")
		self.ui.setupUi(icon_settings)
		self.ui.set_title(title)
		self.ui.set_text(text)
		self.ui.set_ok_text(ok_text)
		self.ui.set_no_text(no_text)
		self.center()
		'''
		self.createContextMenu()
		self.ui.text_label.setContextMenuPolicy(Qt.CustomContextMenu)
		self.ui.text_label.customContextMenuRequested.connect(self.showContextMenu)
		'''
		self.ui.button_no.clicked.connect(self.NoClicked)
		self.ui.button_ok.clicked.connect(self.OkClicked)
		self.show()
	
	'''
	def createContextMenu(self):
		self.context_menu = QMenu(self)
		self.copy_action = QAction("Copy", self)
		#self.copy_action.triggered.connect(self.copyText)
		# self.copy_action.setShortcut(QKeySequence("Ctrl+c"))
		self.context_menu.addAction(self.copy_action)
		self.paste_action = QAction("Paste", self)
		#self.paste_action.triggered.connect(self.pasteText)
		# self.paste_action.setShortcut(QKeySequence("Ctrl+v"))
		self.context_menu.addAction(self.paste_action)
	
	#def copyText(self):
	#	# Copy selected text to clipboard
	#	self.text_edit.copy()
	
	#def pasteText(self):
	#	# Paste text from clipboard
	#	self.text_edit.paste()
	
	def showContextMenu(self, pos):
		self.context_menu.exec_(self.ui.text_label.mapToGlobal(pos))
	'''
	
	'''
	def contextMenuEvent(self, event):
		context_menu = QMenu(self)
		action1 = context_menu.addAction("Action 1")
		action2 = context_menu.addAction("Action 2")
		action3 = context_menu.addAction("Action 3")
		action = context_menu.exec_(self.mapToGlobal(event.pos()))
		if action == action1:
			print("Action 1 selected")
		elif action == action2:
			print("Action 2 selected")
		elif action == action3:
			print("Action 3 selected")
	'''
	
	def NoClicked(self):
		self.isqestion = False
		#QCoreApplication.exit(0)

	'''
	def open_file_dialog(self):
		# fileName = QtWidgets.QFileDialog.getSaveFileName(parent=None, caption="Заголовок окна", directory="c:\\Python34", filter="All Files (*);;Python Files (*.py);;Text Files (*.txt)", initialFilter="Text Files (*.txt)")
		# if fileName != "":
		#	lineEdit1.setText(fileName)
		filename, _ = QFileDialog.getOpenFileName(self, "Select a File", r"./", "Images (*.png *.jpg)")
		return filename
	'''

	def OkClicked(self):
		self.isqestion = True
		#QCoreApplication.exit(0)
		#fname = self.open_file_dialog()
		#print(fname)
		#fdir = QFileDialog.getExistingDirectory(None, 'Select a folder:', '')
		#print(fdir)
		
	def resize_form(self):
		self.ui.set_size(self.ui.text_label.width() + 22, self.ui.text_label.height() + 30)
	
	#def closeEvent(self, event):
		# Ваш код для завершения процессов
		# event.accept()  # Закрыть окно

def main():
	import pathlib
	import sys
	icon_settings = {
						'forms': str(pathlib.Path(sys.argv[0]).parent.joinpath('img').joinpath('excel.svg')),
						'html': str(pathlib.Path(sys.argv[0]).parent.joinpath('img').joinpath('html.svg')),
						'clear': str(pathlib.Path(sys.argv[0]).parent.joinpath('img').joinpath('clear.png')),
						'refresh': str(pathlib.Path(sys.argv[0]).parent.joinpath('img').joinpath('refresh.png')),
						'save': str(pathlib.Path(sys.argv[0]).parent.joinpath('img').joinpath('save.png')),
						'uses': str(pathlib.Path(sys.argv[0]).parent.joinpath('img').joinpath('uses.png')),
						'zip': str(pathlib.Path(sys.argv[0]).parent.joinpath('img').joinpath('zip.png')),
					}
	#print(icon_settings)
	app = QApplication([])
	#question_window = QuestionForm(icon_settings, title = "Question", text = "The text of question!", ok_text = "Да", no_text = "Нет")
	#question_window.resize_form()
	#settings_window = SettingsForm(icon_settings, title = "Настройки")
	
	app.exec()
	# clipboard = QApplication.clipboard()
	# clipboard.setText("Hello, world!")
	# text = clipboard.text()
	# QTextEdit.copy()
	#
	## settings_form.setObjectName("settings_form")
	#
	
if __name__ == '__main__':
	main()
