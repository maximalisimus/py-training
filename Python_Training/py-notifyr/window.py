#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import json
import configparser
import argparse
import tkinter as tk
from tkinter import ttk
from tkinter import font as fnt
from enum import Enum
import time
import platform
import socket
import shutil
import base64
from multiprocessing.managers import BaseManager
import signal
import os
import threading
import subprocess

import tasks

from PIL import Image, ImageTk
# bmp ico jpg png tga

__author__ = 'Mikhail Artamonov'
__description__ = 'Cross-platform graphical desktop notifications and reminders based on Tk/Tcl.'
__progname__ = str(pathlib.Path(sys.argv[0]).resolve())
__copyright__ = f"© The \"{__progname__}\". Copyright  by 2024."
__credits__ = ["Mikhail Artamonov"]
__license__ = "GPL3"
__version__ = "1.0.0"
__maintainer__ = "Mikhail Artamonov"
__status__ = "Production"
__date__ = '11.10.2022'
__modifed__ = '22.07.2024'

class Ru_Eng:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return {
				'ru': {
							'description': 'Кросс-платформенные графические уведомления и напоминания на рабочем столе на основе Tk/Tcl.',
							'version': 'Версия',
							'info': 'Информация об авторе.',
							'lng': 'Язык интерфейса (по умолчанию: русский).',
							'console': 'Оболочка по умолчанию.',
							'ontime': 'Время, по истечении которого уведомление автоматически закроется (по умолчанию 5000).',
							'notimer': 'Отключение таймера автоматического закрытия уведомления.',
							'style': 'Стиль отображения окна (полный, компактный, по умолчанию: компактный).',
							'distance': 'Расстояние между окнами соседних уведомлений.',
							'alpha': 'Прозрачность формы.',
							'sub_title': 'Управление',
							'sub_desc': 'Команды управления.',
							'sub_help': 'Помощь по командам.',
							'systemd': {
											'info': 'Службы systemd.',
											'create': "Создать «pynotifyr.service».",
											'delete': "Удалить «pynotifyr.service».",
											'status': "Статус «pynotifyr.service».",
											'enable': "Включить «pynotifyr.service».",
											'disable': "Выключить «pynotifyr.service».",
											'start': "Запустить «pynotifyr.service».",
											'stop': "Остановить «pynotifyr.service».",
											'reload': "Перезагрузить «pynotifyr.service»."
										},
							'daemon': {
											'info': 'Управление демоном.',
											'start': 'Запустить демон.',
											'stop': 'Остановить демон.',
											'restart': 'Перезагрузить демон.',
											'kill': 'Убить демона.'
										},
							'title_group': 'Заголовок',
							'title_info': 'Управление заголовком.',
							'title': 'Название уведомления (заголовок).',
							'tfamily': 'Шрифт заголовка (по умолчанию: Arial).',
							'tsize': 'Размер шрифта заголовка (по умолчанию: 12).',
							'tweight': 'Тип шрифта заголовка (по умолчанию: жирный).',
							'tund': 'Подчеркните текст заголовка (0 отсутствует, 1 присутствует, по умолчанию: 0).',
							'tslant': 'Наклон (italic) текста заголовка (по умолчанию: нормальный, т.е. ровный).',
							'tstrike': 'Зачеркнутый шрифт. Аналогично настройке подчеркивания (по умолчанию: 0).',
							'tcolor': 'Цвет текста заголовка (по умолчанию: черный).',
							'mess_group': 'Уведомления',
							'mess_info': 'Управления уведомлениями.',
							'text': 'Текст уведомления.',
							'bg': 'Цвет фона окна уведомлений.',
							'bcolor': 'Цвет текста уведомления.',
							'bfamily': 'Шрифт текста уведомления (по умолчанию: Arial).',
							'bsize': 'Размер шрифта уведомления (по умолчанию: 12).',
							'bweight': 'Тип шрифта уведомления (жирный, нормальный, по умолчанию: нормальный).',
							'bund': 'Подчеркивание текста уведомления (0 отсутствует, 1 присутствует, по умолчанию: 0).',
							'bslant': 'Наклон (italic) шрифта текста уведомления (обычный, курсив, по умолчанию: обычный).',
							'bstrike': 'Зачеркнутый шрифт. Аналогично настройке подчеркивания (по умолчанию: 0).',
							'icon_group': 'Иконка',
							'icon_info': 'Управление иконками.',
							'icon': 'Файл иконки внутри формы (по умолчанию: None).',
							'close': 'Файл иконки закрытия (крестика) окна уведомления (по умолчанию: default).',
							'scale': 'Масштабирование иконки внутри формы (Пожалуйста, укажите 2 значения через запятую без пробелов. Например, 32,32. По умолчанию: 48,48).',
							'clscale': 'Масштабирование иконки закрытия (крестика) окна уведомления (Пожалуйста, укажите 2 значения через запятую без пробелов. Например, 32,32. По умолчанию: 24,24).',
							'offset_group': 'Положение',
							'offset_info': 'Положения и перемещения.',
							'posx': 'Положение окна уведомлений на рабочем столе по оси X (слева, по центру и справа. По умолчанию: справа).',
							'posy': 'Положение окна уведомлений на рабочем столе вдоль оси Y (вверху, по центру и внизу. По умолчанию: вверху).',
							'x': 'Переместите окно уведомления на указанную величину вдоль оси X (по умолчанию: 0).',
							'y': 'Переместите окно уведомления на указанную величину вдоль оси Y (по умолчанию: 0).',
							'relative': 'Считайте координаты сдвига вдоль осей относительными, в противном случае абсолютными (по умолчанию: относительные).',
							'topmost': 'Поверх других окон (по умолчанию: False).',
							'config': {
										'info': 'Настройки программы.',
										'show': 'Показать список доступных тем.',
										'dirs': 'Показать каталог расположения тем.',
										'save': 'Сохраните настройки.',
										'load': 'Загрузить настройки.',
										'reset': 'Сбросить все изменения.',
										'theme': 'Файл JSON с цветовой схемой отображения уведомлений (например, dark.json или light.json).',
										'output': 'Файл сохранения темы.'
									}
						},
				'eng': {
							'description': 'Cross-platform graphical desktop notifications and reminders based on Tk/Tcl.',
							'version': 'Version.',
							'info': 'Information about the author.',
							'lng': 'Interface language (Default: ru).',
							'console': 'The default shell.',
							'ontime': 'The time after which the notification will automatically close (5000 by default).',
							'notimer': 'Turning off the timer for automatic closing of the notification.',
							'style': 'Window display style (full, compact, Default: compact).',
							'distance': 'The distance between the windows of neighboring notifications.',
							'alpha': 'Transparency of the form.',
							'sub_title': 'Management',
							'sub_desc': 'Management commands.',
							'sub_help': 'commands help.',
							'systemd': {
											'info': 'Systemd management.',
											'create': "Create «pynotifyr.service».",
											'delete': "Delete «pynotifyr.service».",
											'status': "Status «pynotifyr.service».",
											'enable': "Enable «pynotifyr.service».",
											'disable': "Disable «pynotifyr.service».",
											'start': "Start «pynotifyr.service».",
											'stop': "Stop «pynotifyr.service».",
											'reload': "Reload «pynotifyr.service»."
										},
							'daemon': {
											'info': 'Daemon control.',
											'start': 'Start daemon.',
											'stop': 'Stop daemon.',
											'restart': 'Restart daemon.',
											'kill': 'Kill daemon.'
										},
							'title_group': 'Title',
							'title_info': 'Title control.',
							'title': 'The title of the notification.',
							'text': 'The text of the notification.',
							'tfamily': 'The font of the title.',
							'tsize': 'The font size of the title (default: 12).',
							'tweight': 'The font type of the title (default: bold).',
							'tund': 'Underline the title text (0 is missing, 1 is present, default: 0).',
							'tslant': 'The font tilt of the title text (Default: roman).',
							'tstrike': 'The crossed-out font. Similar to the underscore setting (Default: 0).',
							'tcolor': 'The color of the title text (default: black).',
							'mess_group': 'Notification',
							'mess_info': 'Notification control.',
							'bg': 'The background color of the notification window.',
							'bcolor': 'The color of the notification text.',
							'bfamily': 'The font of the notification text.',
							'bsize': 'The font size of the notification text (default: 12).',
							'bweight': 'The font type of the notification (bold, normal, default: normal).',
							'bund': 'Underline the notification text (0 is missing, 1 is present, default: 0).',
							'bslant': 'The font tilt of the notification text (normal, italics, Default: roman).',
							'bstrike': 'The crossed-out font. Similar to the underscore setting (Default: 0).',
							'icon_group': 'Icon',
							'icon_info': 'Icon control.',
							'icon': 'The icon file inside the form (default: None).',
							'close': 'The file of the notification window (cross) closing icon (default: default).',
							'scale': 'Scaling of the central notification icon (please write 2 integers separated by commas without spaces. For example, 32,32. Dafault: 48,48).',
							'clscale': 'Scaling of the notification window close button icon (please write 2 integers separated by commas without spaces. For example, 32,32. Dafault: 24,24).',
							'offset_group': 'Offset',
							'offset_info': 'Offsets and Movements.',
							'posx': 'The position of the notification window on the desktop on the X axis (left, center and right. Default: right).',
							'posy': 'The position of the notification window on the desktop along the Y axis (top, center and bottom. Default: top).',
							'x': 'Move the notification window by the specified value along the X-axis (Default: 0).',
							'y': 'Move the notification window by the specified value along the Y axis (Default: 0).',
							'relative': 'Consider the coordinates of the shift along the axes relative, otherwise absolute (Default: True).',
							'topmost': 'On top of other windows (default: False).',
							'config': {
										'info': 'Program Settings.',
										'show': 'Show a list of available topics.',
										'dirs': 'Show the themes location directory.',
										'load': 'Download Settings.',
										'save': 'Save Settings.',
										'reset': 'Reset Settings.',
										'theme': 'A JSON file of the notification display color scheme (for example, dark.json or light.json).',
										'output': 'The theme save file.'
									}
						}
			}

class Default_Lang:
	
	Lang = Ru_Eng()
	
	def __repr__(self):
		return f"{self.__class__}: {self.Lang}"
	
	def __str__(self):
		return f"{self.Lang}"
	
	def __call__(self):
		return f"{self.Lang}"

class Prog_Name:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return str(pathlib.Path(__progname__).name).split('.')[0]

class Full_Prog:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return str(pathlib.Path(__progname__).resolve())

class ProgName:
	
	name = Prog_Name()
	full = Full_Prog()

class SystemdText:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"[Unit]\n" +\
				f"Description={__description__}\n" +\
				f"Wants=graphical.target\n" +\
				f"After=graphical.target\n\n" +\
				f"[Service]\n" +\
				f"Type=simple\n" +\
				f"RemainAfterExit=no\n" +\
				f"ExecStart={ProgName.name} daemon -run\n" +\
				f"ExecStop={ProgName.name} daemon -stop\n" +\
				f"ExecReload={ProgName.name} daemon -restart\n\n" +\
				f"[Install]\n" +\
				f"WantedBy=multi-user.target"

class Service_File:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return pathlib.Path('/etc/systemd/system/pynotifyr.service').resolve()

class SystemdConfig:
	
	config = SystemdText()
	service = Service_File()

	@classmethod
	def control(cls, console, select = None):
		service_info, service_err = SHELL.shell_open(console, cls.commands(select))
		return service_info, service_err
	
	@classmethod
	def create_service(cls):
		if not cls.service.exists():
			Files.read_write_file(cls.service, 'w', cls.config)

	@classmethod
	def remove_service(cls, console):
		print('Stop service ...')
		service, err = cls.control(console, 'stop')
		if service != '':
			print(service)
		if err != '':
			print('Error:\n', err)
		print('Disable service ...')
		service, err = cls.control(console, 'disable')
		if service != '':
			print(service)
		if err != '':
			print('Error:\n', err)
		print('Delete service ...')
		cls.service.unlink(missing_ok=True)
		print('Systemd  daemon-reload...')
		service, err = cls.control(console, 'restart')
		if service != '':
			print(service)
		if err != '':
			print('Error:\n', err)

	@staticmethod
	def systemd_question(argv):
		if argv.status:
			return 'status'
		if argv.enable:
			return 'enable'
		if argv.disable:
			return 'disable'
		if argv.start:
			return 'start'
		if argv.stop:
			return 'stop'
		if argv.reload:
			return 'reload'
		return 'empty'

	@staticmethod
	def commands(case = None):
		''' Systemd control selection. '''
		return {
				'status': f"sudo systemctl status pynotifyr.service",
				'start': f"sudo systemctl start pynotifyr.service",
				'stop': f"sudo systemctl stop pynotifyr.service",
				'reload': f"sudo systemctl restart pynotifyr.service",
				'enable': f"sudo systemctl enable pynotifyr.service",
				'disable': f"sudo systemctl disable pynotifyr.service",
				'restart': f"sudo systemctl daemon-reload",
		}.get(case, f"sudo systemctl daemon-reload")

class AuthorInfo:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"Author: {__author__}\nProgname: {__progname__}\nVersion: {__version__}\n" + \
			f"Description: {__description__}\n" +\
			f"Date of creation: {__date__}\nLast modified date: {__modifed__}\n" + \
			f"License: {__license__}\nCopyright: {__copyright__}\nCredits: {__credits__}\n" + \
			f"Maintainer: {__maintainer__}\nStatus: {__status__}\n"

class Author:
	
	Info = AuthorInfo()
	
	def __repr__(self):
		return f"{self.__class__}: {self.Info}"
	
	def __str__(self):
		return f"{self.Info}"
	
	def __call__(self):
		return f"{self.Info}"

class NoValue(Enum):
	''' Base Enum class elements '''

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class Weight(NoValue):
	''' Weight parameter fonts '''
	normal = 'normal'
	bold = 'bold'
	
	@classmethod
	def GetWeightValue(cls, value: str):
		''' Get Weight to value elements '''
		for x in cls:
			if value == x.value:
				return x
		return None

	@classmethod
	def GetWeightName(cls, on_name):
		''' Get Weight to name elements '''
		for x in cls:
			if on_name == x:
				return x
		return None

class Slant(NoValue):
	''' Italic text or normal mode '''
	Normal = 'roman'
	Italic = 'italic'
	
	@classmethod
	def GetSlantValue(cls, value: str):
		''' Get PositionX to value elements '''
		for x in cls:
			if value == x.value:
				return x
		return None

	@classmethod
	def GetSlantName(cls, on_name):
		''' Get PositionX to name elements '''
		for x in cls:
			if on_name == x:
				return x
		return None

class PositionX(NoValue):
	''' Horizontal Position Desktop '''
	Left = 'left'
	Right = 'right'
	Center = 'center'
	
	@classmethod
	def GetPosValue(cls, value: str):
		''' Get PositionX to value elements '''
		for x in cls:
			if value == x.value:
				return x
		return None

	@classmethod
	def GetPosName(cls, on_name):
		''' Get PositionX to name elements '''
		for x in cls:
			if on_name == x:
				return x
		return None

class PositionY(NoValue):
	''' Vertical Position Desktop '''
	Top = 'top'
	Center = 'center'
	Bottom = 'bottom'

	@classmethod
	def GetPosValue(cls, value: str):
		''' Get PositionY to value elements '''
		for x in cls:
			if value == x.value:
				return x
		return None

	@classmethod
	def GetPosName(cls, on_name):
		''' Get PositionY to name elements '''
		for x in cls:
			if on_name == x:
				return x
		return None

class FormStyle(NoValue):
	''' Form Style '''
	
	Standart = 'standart'
	Compact = 'compact'
	
	@classmethod
	def GetFormStyleValue(cls, value: str):
		''' Get Form Style to value elements '''
		for x in cls:
			if value == x.value:
				return x
		return None

	@classmethod
	def GetFormStyleName(cls, on_name):
		''' Get Form Style to name elements '''
		for x in cls:
			if on_name == x:
				return x
		return None

class HostName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return 'localhost'

class CheckAccess:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return 'py-notifyr'

class CMD_Platform:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		python = str(pathlib.Path(str(sys.executable)).resolve())
		script = str(pathlib.Path(str(ProgName.full)).resolve())
		cmd = []
		if  platform.system() == 'Windows':			
			cmd = ('start', '/b', python, script, 'daemon', '-run')
		else:
			cmd = (python, script, 'daemon', '-run', '&')
		return cmd

class CMD:
	
	line = CMD_Platform()
	
	def __repr__(self):
		return f"{self.__class__}: {self.line}"
	
	def __str__(self):
		return f"{self.line}"
	
	def __call__(self):
		return f"{self.line}"

class SetPID:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return os.getpid()

class Boolean:
	
	@classmethod
	def verify_bool(cls, value):
		if type(value) != bool:
			raise TypeError('Enter the boolean!')
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: str):
		self.verify_bool(value)
		setattr(instance, self.name, value)

class Strings:
	
	@classmethod
	def verify_str(cls, value):
		if type(value) != str:
			raise TypeError('Enter the string!')
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: str):
		self.verify_str(value)
		setattr(instance, self.name, value)

class Integer:
	
	@classmethod
	def verify_int(cls, value):
		if type(value) != int:
			raise TypeError('Enter the integer!')
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: int):
		self.verify_int(value)
		setattr(instance, self.name, value)

class Texts:
	
	Access = CheckAccess()
	
	def __repr__(self):
		return f"{self.__class__}: {self.Access}"
	
	def __str__(self):
		return f"{self.Access}"
	
	def __call__(self):
		return f"{self.Access}"
	
	@staticmethod
	def StrToBase(inputSTR: str):
		str_bytes = inputSTR.encode('utf-8')
		return base64.b64encode(str_bytes)
	
	@staticmethod
	def BaseToSTR(inputBase: str):
		data = base64.b64decode(inputBase)
		return data.decode('utf-8')

class SHELL:
	
	@staticmethod
	def shell_open(shell: str, cmd: str):
		''' Execute the command in the specified command shell. 
			Returns the result of executing the command, if any.'''
		proc = subprocess.Popen(shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
		sys.stdout.flush()
		proc.stdin.write(cmd + "\n")
		proc.stdin.close()
		out_data = f"{proc.stdout.read()}"
		err_data = f"{proc.stderr.read()}"
		# Close the 'Popen' process correctly
		proc.terminate()
		proc.kill()
		return out_data, err_data

	@staticmethod
	def shell_run(cmd):
		result = subprocess.run(cmd, shell=True)
		return result

class Meta(type):
	
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@property
	def prefix_icon_folder(cls):
		return f"py-notifyr-icons"
	
	@property
	def LangFileName(cls):
		return f"language.json"
	
	@property
	def access_key(cls):
		return Texts.StrToBase(Texts.Access)
	
	@property
	def SockFileName(cls):
		return f"pynotifyr.sock"
	
	@property
	def MainThemeName(cls):
		return f"standart.json"
	
	@property
	def LightThemeName(cls):
		return f"light.json"
	
	@property
	def DarkThemeName(cls):
		return f"dark.json"
	
	@property
	def PREFIX(cls):
		return pathlib.Path(sys.argv[0]).resolve().parent

	@property
	def koef_x(cls):
		return {'left': 1, 'center': 1, 'right': -1}
		
	@property
	def koef_y(cls):
		return {'top': 1, 'center': 1, 'bottom': -1}

class Defaults(metaclass=Meta):
	''' Class Defaults 
	
		Info: The default value class.
		Variables:
			PREFIX: The directory where the program 
					was launched from.
			config_file: The default settings file, 
						which is located in the same directory 
						as the program itself.
			koef_x: The X-axis coefficient used in calculating 
					the new location of the form, 
					if at least one has already been launched.
			koef_y: The Y-axis coefficient used in calculating 
					the new location of the form, 
					if at least one has already been launched.
		Methods:
			CalcPositionX(pos_x: str, scr_width: int, width: int):
				Calculation of the standard position by X (Left).
				pos_x = "left", "center" or "right"
			
			CalcPositionY(pos_y: str, scr_height: int, height: int):
				Calculation of the standard position by Y (Top).
				pos_y = "top", "center" or "bottom"
			
			CalcNewPosition(scr_width: int, scr_height: int, 
					pos_x: str, pos_y: str, width: int, 
					height: int, left: int, top: int):
				Calculation of the new position of the form 
				in the specified previous position. 
				The previous position can be ready, 
				for example, using the socket library.
	'''

	@staticmethod
	def CalcPositionX(pos_x: str, scr_width: int, width: int):
		''' Calculate Position Left (x) '''
		if PositionX.GetPosValue(pos_x) == PositionX.Left:
			calc_x = 0
		elif PositionX.GetPosValue(pos_x) == PositionX.Center:
			calc_x = int(scr_width/2) - int(width/2)
		else:
			calc_x = scr_width - width
		return calc_x

	@staticmethod
	def CalcPositionY(pos_y: str, scr_height: int, height: int):
		''' Calculate Position Top (y) '''
		if PositionY.GetPosValue(pos_y) == PositionY.Top:
			calc_y = 0
		elif PositionY.GetPosValue(pos_y) == PositionY.Center:
			calc_y =  int(scr_height/2) - int(height/2)
		else:
			calc_y = scr_height - height
		return calc_y

	@classmethod
	def CalcNewPosition(cls, scr_width: int, scr_height: int, 
					pos_x: str, pos_y: str,  
					width: int, height: int, 
					left: int, top: int, distance: int = 10):
		''' Calculation for new position to Form '''
		virt_x = width + distance
		virt_y = height + distance
		real_x = virt_x * cls.koef_x[pos_x] + left
		real_y = virt_y * cls.koef_y[pos_y] + top
		if PositionY.GetPosValue(pos_y) == PositionY.Bottom:
			if real_y < 0:
				real_y = cls.CalcPositionY(pos_y, scr_height, height)
			else:
				real_x = left
		else:
			if (scr_height - real_y) < height:
				real_y = cls.CalcPositionY(pos_y, scr_height, height)
			else:
				real_x = left
		return real_x, real_y

class FilesMeta(type):
	
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@property
	def language_file(cls):
		return Defaults.PREFIX.joinpath(Defaults.LangFileName)
	
	@property
	def prefix_icon(cls):
		return Defaults.PREFIX.joinpath(Defaults.prefix_icon_folder)
	
	@property
	def dark_theme(cls):
		return cls.ThemeDir.joinpath(Defaults.DarkThemeName)

	@property
	def default_theme(cls):
		return cls.ThemeDir.joinpath(Defaults.MainThemeName)

	@property
	def light_theme(cls):
		return cls.ThemeDir.joinpath(Defaults.LightThemeName)

	@property
	def socket_file(cls):
		return cls.ConfigDir.joinpath(cls.SockFileName)

	@property
	def ConfigDir(cls):
		if platform.system() == 'Linux':
			return pathlib.Path.home().joinpath('.config').joinpath('py-notifyr')
		elif  platform.system() == 'Windows':
			return pathlib.Path.home().joinpath('AppData').joinpath('Roaming').joinpath('py-notifyr')
		else:
			return pathlib.Path.home().joinpath('.config').joinpath('py-notifyr') 

	@property
	def ConfigFileName(cls):
		return cls.ConfigDir.joinpath('theme').joinpath('config.ini')

	@property
	def ThemeDir(cls):
		return cls.ConfigDir.joinpath('theme').joinpath('theme-path')
	
	@property
	def ThemeIcons(cls):
		return cls.ConfigDir.joinpath('theme').joinpath('theme-icons')

	@property
	def SockFileName(cls):
		return f"pynotifyr.sock"

class Files(metaclass=FilesMeta):
	
	@staticmethod
	def check_pid(pid):
		""" Check For the existence of a unix pid. """
		ischeck = False
		try:
			os.kill(pid, 0)
			ischeck = True
		except:
			ischeck = False
		else:
			ischeck = True
		return ischeck
	
	@classmethod
	def CreateClientServer(cls):
		client_and_server = ClientServer()
		if not cls.socket_file.exists():
			client_and_server.set_free_port(cls.socket_file)
			del client_and_server
			client_and_server = ClientServer()
			client_and_server.set_free_port(cls.socket_file)
		else:
			client_and_server.set_free_port(cls.socket_file)
		return client_and_server
	
	@staticmethod
	def read_write_json(jfile, typerw, data = dict(), indent: int = 2):
		''' The function of reading and writing JSON objects. '''
		file_save = pathlib.Path(str(jfile)).resolve()
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with open(str(file_save), typerw) as fp:
			if 'r' in typerw:
				data = json.load(fp)
				return data
			else:
				json.dump(data, fp, indent=indent)

	@staticmethod
	def read_write_file(onfile, typerw, data = ""):
		''' The function of reading and writing text files. '''
		file_save = pathlib.Path(str(onfile)).resolve()
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with open(str(file_save), typerw) as fp:
			if 'r' in typerw:
				data = fp.read()
				return data
			else:
				fp.write(data)

	@staticmethod
	def read_write_config(cfile, typerw, data: configparser.ConfigParser):
		file_save = pathlib.Path(str(cfile)).resolve()
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with open(str(file_save), typerw) as configfile:
			if 'r' in typerw:
				data.read_file(configfile)
			else:
				data.write(configfile)

	@staticmethod
	def JSONToSTR(data_json: dict) -> str:
		return json.dumps(data_json, indent=2)
	
	@staticmethod
	def STRToJSON(value: str) -> dict:
		return json.loads(value)

class Base:
	
	__slots__ = ['__dict__']
		
	def __init__(self):
		self.except_list = []
	
	def __str__(self):
		''' For STR Function output paramters. '''
		return '\t' + '\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in self.except_list and '__' not in x)
	
	def __repr__(self):
		''' For Debug Function output paramters. '''
		return f"{self.__class__}:\n\t" + \
				'\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in self.except_list and '__' not in x)

class Arguments(Base):
	''' The class of the set of input parameters. '''
	
	def __init__(self, *args, **kwargs):
		super(Arguments, self).__init__()
		self.except_list.append('except_list')
		self.except_list.extend('Reset ApplyTheme SaveTheme CreateDefaultConfig SaveConfig LoadConfig Search_Socket_Pos'.split())
		self.except_list.extend('show dirs save reset output FormPos SocketFormPos ThemeDict FixArgs'.split())
		self.except_list.extend('notimer ontime theme title text style alpha'.split())
		self.except_list.extend('tfamily tsize tweight tund tslant tstrike tcolor'.split())
		self.except_list.extend('bg bcolor bfamily bsize bweight bund bslant bstrike'.split())
		self.except_list.extend('close clscale posx posy x y relative topmost'.split())
		self.except_list.extend('info Lang lng noprefix Theme parser_dict'.split())
		'''
		self.Title = args[0] if len(args) >= 1 else kwargs.get('Title','Apps')
		self.Message = args[1] if len(args) >= 2 else kwargs.get('Message','Info!')
		self.OnTime = args[2] if len(args) >= 3 else kwargs.get('OnTime', 5000)
		self.isTimer = args[3] if len(args) >= 4 else kwargs.get('isTimer',True)
		self.icon = args[4] if len(args) >= 5 else kwargs.get('icon','None')
		self.TFFamily = args[5] if len(args) >= 6 else kwargs.get('TFFamily','Arial')
		self.TFSize = args[6] if len(args) >= 7 else kwargs.get('TFSize', 12)
		self.TFWeight = args[7] if len(args) >= 8 else kwargs.get('TFWeight','bold')
		self.TFUnderline = args[8] if len(args) >= 9 else kwargs.get('TFUnderline', 0)
		self.TFSlant = args[9] if len(args) >= 10 else kwargs.get('TFSlant','roman')
		self.TFOverstrike = args[10] if len(args) >= 11 else kwargs.get('TFOverstrike',0)
		self.TitleFG = args[11] if len(args) >= 12 else kwargs.get('TitleFG','black')
		self.BFFamily = args[12] if len(args) >= 13 else kwargs.get('BFFamily','Arial')
		self.BFSize = args[13] if len(args) >= 14 else kwargs.get('BFSize', 12)
		self.BFWeight = args[14] if len(args) >= 15 else kwargs.get('BFWeight','normal')
		self.BFUnderline = args[15] if len(args) >= 16 else kwargs.get('BFUnderline', 0)
		self.BFSlant = args[16] if len(args) >= 17 else kwargs.get('BFSlant','roman')
		self.BFOverstrike = args[17] if len(args) >= 18 else kwargs.get('BFOverstrike', 0)
		self.BG = args[18] if len(args) >= 19 else kwargs.get('BG','#FFFADD')
		self.BodyFG = args[19] if len(args) >= 20 else kwargs.get('BodyFG','black')
		self.scale = args[20] if len(args) >= 21 else kwargs.get('scale', '24,24')
		self.PosX = args[21] if len(args) >= 22 else kwargs.get('PosX', 'right')
		self.PosY = args[22] if len(args) >= 23 else kwargs.get('PosY', 'top')
		self.Alpha = args[23] if len(args) >= 24 else kwargs.get('Alpha', 1.0)
		self.MoveX = args[24] if len(args) >= 25 else kwargs.get('MoveX', 0)
		self.MoveY = args[25] if len(args) >= 26 else kwargs.get('MoveY', 0)
		self.Relative = args[26] if len(args) >= 27 else kwargs.get('Relative', True)
		self.Topmost = args[27] if len(args) >= 28 else kwargs.get('Topmost', False)
		self.save = args[28] if len(args) >= 29 else kwargs.get('save', False)
		self.reset = args[29] if len(args) >= 30 else kwargs.get('reset', False)
		self.CloseIcon = args[30] if len(args) >= 31 else kwargs.get('CloseIcon', 'default')
		self.Theme = args[31] if len(args) >= 32 else kwargs.get('Theme', '')
		self.isTheme = args[32] if len(args) >= 33 else kwargs.get('isTheme', False)
		self.output = args[33] if len(args) >= 34 else kwargs.get('output', '')
		self.Style = args[34] if len(args) >= 35 else kwargs.get('Style', 'standart')
		self.ScaleClose = args[35] if len(args) >= 36 else kwargs.get('ScaleClose', '24,24')
		self.distance = args[36] if len(args) >= 37 else kwargs.get('distance', 10)
		'''
		self.FormPos = dict()
		self.SocketFormPos = dict()
		self.ThemeDict = dict()
		self.LoadConfig()
		if Files.language_file.exists():
			self.Lang = Files.read_write_json(Files.language_file, 'r')
		else:
			self.Lang = Default_Lang.Lang
	
	def Search_Socket_Pos(self, task_list):
		for z in range(len(task_list)-1, 0, -1):
			if type(task_list[z]) == dict:
				if task_list[z].get('position_x', '') == self.PosX and task_list[z].get('position_y', '') == self.PosY:
					return task_list[z]
		return dict()
	
	def SaveConfig(self):
		self.SaveTheme()
		if not Files.ConfigFileName.exists():
			Files.ConfigFileName.parent.mkdir(parents=True,exist_ok=True)
		config = configparser.ConfigParser()
		config['Main'] = {'Theme': str(self.Theme), 'Lang': str(self.lng)}
		Files.read_write_config(str(Files.ConfigFileName), 'w', config)
	
	def LoadConfig(self):
		if Files.ConfigFileName.exists():
			temp_theme = f"{self.Theme}"
			config = configparser.ConfigParser()
			Files.read_write_config(str(Files.ConfigFileName), 'r', config)
			self.Theme = config['Main']['Theme']
			self.lng = config['Main']['Lang']
			self.ApplyTheme()
			self.Theme = f"{temp_theme}"
		else:
			self.lng = 'ru'
	
	def CreateDefaultConfig(self):
		dark_theme = Files.dark_theme
		light_theme = Files.light_theme
		
		theme_str = f"{self.Theme}"
		self.icon = pathlib.Path(str(self.icon)).resolve() if self.icon != '' and self.icon != 'None' else self.icon
		self.CloseIcon = pathlib.Path(str(self.CloseIcon)).resolve() if self.CloseIcon != '' and self.CloseIcon != 'default' else self.CloseIcon
		
		temp_theme = dict()
		for k, v in self.__dict__.items():
			if not k in self.except_list and '__' not in k:
				if type(v) in [str, float, bool, int]:
					temp_theme[k] = v
				elif 'value' in dir(v):
					temp_theme[k] = v.value
				else:
					temp_theme[k] = str(v)
		
		self.Reset()
		self.BG = '#303030'
		self.TitleFG = 'white'
		self.BodyFG = 'white'
		self.Alpha = 0.8
		self.TFSize = 12
		self.BFSize = 12
		self.scale = '48,48'
		self.ScaleClose = '24,24'
		self.PosX = 'right'
		self.PosY = 'top'
		self.MoveX = 0
		self.MoveY = 0
		self.OnTime = 5000
		self.Style = 'compact'
		
		'''
		cur_icon = Defaults.PREFIX.joinpath('info.png').resolve()
		cur_close_icon = Defaults.PREFIX.joinpath('exit_close_24x24.png').resolve()
		self.icon = Files.ThemeIcons.joinpath('info.png').resolve()
		self.CloseIcon = Files.ThemeIcons.joinpath('exit_close_24x24.png').resolve()
		
		self.icon.parent.mkdir(parents=True,exist_ok=True)
		
		if self.icon.exists():
			self.icon.unlink(missing_ok=True)
		
		if self.CloseIcon.exists():
			self.CloseIcon.unlink(missing_ok=True)
		
		shutil.copy(cur_icon, self.icon)
		shutil.copy(cur_close_icon, self.CloseIcon)
		'''
		if Files.prefix_icon.exists():
			Files.ThemeIcons.mkdir(parents=True,exist_ok=True)
			all_icon = Files.prefix_icon.glob('*.png')
			for icons in all_icon:
				new_icon = Files.ThemeIcons.joinpath(str(icons.name))
				if new_icon.exists():
					new_icon.unlink(missing_ok=True)
				shutil.copy(icons, new_icon)
		
		self.noprefix = True
		temp_output = f"{self.output}"
		
		self.output = dark_theme
		
		self.SaveTheme()
				
		self.BG = '#FFFADD'
		self.TitleFG = 'black'
		self.BodyFG = 'black'
		self.Alpha = 0.8
		self.Style = 'compact'
		
		self.output = light_theme
		
		self.SaveTheme()
		
		self.Theme = light_theme	
		self.SaveConfig()
		
		for k, v in temp_theme.items():
			self.__dict__[k] = v
		
		self.icon = pathlib.Path(str(self.icon)).resolve() if self.icon != '' and self.icon != 'None' else self.icon
		self.CloseIcon = pathlib.Path(str(self.CloseIcon)).resolve() if self.CloseIcon != '' and self.CloseIcon != 'default' else self.CloseIcon
		self.output = f"{temp_output}"
		self.Theme = f"{theme_str}"
		
		self.SaveTheme()
		
		Files.read_write_json(Files.language_file, 'w', Default_Lang.Lang)
	
	def ApplyTheme(self):
		if self.Theme != '':
			self.Theme = pathlib.Path(str(self.Theme)).resolve()
			if self.Theme.exists():
				self.ThemeDict = Files.read_write_json(self.Theme, 'r')
				for k in self.ThemeDict.keys():
					if self.ThemeDict.get(k, '') != '':
						self.__dict__[k] = self.ThemeDict.get(k, '')
		else:
			self.Theme = Files.default_theme
			self.ApplyTheme()
	
	def SaveTheme(self):
		if self.output != '':
			self.output = pathlib.Path(str(self.output)).resolve()
			self.ThemeDict.clear()
			for k, v in self.__dict__.items():
				if not k in self.except_list and '__' not in k:
					if type(v) in [str, float, bool, int]:
						self.ThemeDict[k] = v
					elif 'value' in dir(v):
						self.ThemeDict[k] = v.value
					else:
						self.ThemeDict[k] = str(v)
			Files.read_write_json(self.output, 'w', self.ThemeDict)
		else:
			self.output = Files.default_theme
			self.SaveTheme()
	
	def Reset(self):
		self.Title = 'Apps'
		self.Message = 'Info!'
		self.OnTime = 5000
		self.isTimer = True
		self.icon = 'None'
		self.TFFamily = 'Arial'
		self.TFSize = 14
		self.TFWeight = 'bold'
		self.TFUnderline = 0
		self.TFSlant = 'roman'
		self.TFOverstrike = 0
		self.TitleFG = 'black'
		self.BFFamily = 'Arial'
		self.BFSize = 14
		self.BFWeight = 'normal'
		self.BFUnderline = 0
		self.BFSlant = 'roman'
		self.BFOverstrike = 0
		self.BG = '#FFFADD'
		self.BodyFG = 'black'
		self.scale = '48,48'
		self.PosX = 'right'
		self.PosY = 'top'
		self.Alpha = 1.0
		self.MoveX = 0
		self.MoveY = 0
		self.Relative = True
		self.Topmost = False
		self.save = False
		self.reset = False
		self.CloseIcon = 'default'
		self.Theme = ''
		self.isTheme = False
		self.output = ''
		self.Style = 'compact'
		self.ScaleClose = '24,24'
		self.distance = 10
		self.FormPos.clear()
		self.SocketFormPos.clear()
		self.ThemeDict.clear()
		self.lng = 'ru'
	
	def FixArgs(self):
		self.isTimer = self.notimer
		self.OnTime = self.ontime
		self.Theme = self.theme
		self.Title = self.title
		self.Message = self.text
		self.Style = self.style
		#self.Style = str(FormStyle.GetFormStyleValue(str(self.style)).value)
		self.Alpha = self.alpha
		self.TFFamily = self.tfamily
		self.TFSize = self.tsize
		self.TFWeight = self.tweight
		self.TFUnderline = self.tund
		self.TFSlant = self.tslant
		self.TFOverstrike = self.tstrike
		self.TitleFG = self.tcolor
		self.BG = self.bg
		self.BodyFG = self.bcolor
		self.BFFamily = self.bfamily
		self.BFSize = self.bsize
		self.BFWeight = self.bweight
		self.BFUnderline = self.bund
		self.BFSlant = self.bslant
		self.BFOverstrike = self.bstrike
		self.CloseIcon = self.close
		self.ScaleClose = self.clscale
		self.PosX = self.posx
		self.PosY = self.posy
		self.MoveX = self.x
		self.MoveY = self.y
		self.Relative = self.relative
		self.Topmost = self.topmost
	
	def __getattr__(self, attrname):
		''' Access to a non-existent variable. '''
		return None

class Notify:
	''' Tkinter class form. 
	
		Info: The variables are exactly the same as in Arguments.
				The class is not inherited from Tkinter!
				The class is inherited from the Object type.
		
		Variables:
			root: Tkinter form,
			TitleFont: Title (Header) Form Fonts,
			BodyFont: Body Form Fonts,
			screen_width: Horizontal screen size.
			screen_height: The vertical size of the screen.
			width: The horizontal size of the form.
			height: The vertical size of the form.
			left: The position of the shape on the X-axis.
			top: The position of the shape on the Y-axis.
		
		Methods:
			RelativePosition(self, x: int = 0, y: int = 0): 
				Change the position of the form in relative coordinates.
			
			RealPosition(self, x: int, y: int): 
				Change the position of the form in absolute coordinates.
			
			send(self):
				Show the form on the screen.
	'''
	
	def __init__(self, on_args: Arguments = Arguments()):
		''' Function init tkinter Apps '''
		self.args = on_args
		self.root = tk.Tk()
		
		self.TitleFont = fnt.Font(family = self.args.TFFamily, size = self.args.TFSize, weight = self.args.TFWeight)
		self.TitleFont.configure(underline = self.args.TFUnderline, slant = self.args.TFSlant, overstrike = self.args.TFOverstrike)
		
		self.BodyFont = fnt.Font(family = self.args.BFFamily, size = self.args.BFSize, weight = self.args.BFWeight)
		self.BodyFont.configure(underline = self.args.BFUnderline, slant = self.args.BFSlant, overstrike = self.args.BFOverstrike)
		
		self.style = ttk.Style()
				
		# Window Functions builds
		self.__CreateStyle()
		self.__CreateTitle()
		self.__CreateTransparent()
		self.root.update()
		self.__CreateBtnClose()
		self.__CreateHeader()
		self.__CreateIcon()
		self.__CreateText()
		self.__ElementPack()
		self.__CreatePosition()
		self.root.update()
		
		# Show an opaque form when hovering over the mouse
		self.__FormTimer_Init()
		self.root.bind("<Enter>", self.on_enter)
		self.root.bind("<Leave>", self.on_leave)
			
	def update_clock(self):
		''' Timer on TKinter - finish to destroy application '''
		if not self.timer_flag:
			if self.count <= 0.0:
				self.root.destroy()
			else:
				self.count = float(f"{(self.count - self.counter):.1f}")
				self.root.attributes('-alpha', self.count)
			self.root.after(100, self.update_clock)
		else:
			self.timer_flag = False
			self.root.attributes('-alpha', self.count)
			self.root.after(self.args.OnTime, self.update_clock)
	
	def __FormTimer_Init(self):
		''' Timer on destroy form parameters and functions '''
		self.timer_flag = True
		self.counter = 0.1
		self.count = self.args.Alpha
	
	def on_enter(self, event):
		''' Form focused '''
		self.root.attributes('-alpha', 1.0)
	
	def on_leave(self, enter):
		''' Form not focused '''
		self.root.attributes('-alpha', self.count)
	
	def send(self):
		''' Global Form LOOP - visibility '''
		self.root.update()
		if self.args.isTimer:
			self.update_clock()
		self.root.update()
		self.root.mainloop()
	
	def __CreateTitle(self):
		''' TKinter Title '''
		self.root.title(self.args.Title)
		self.root.configure(bg=self.args.BG)
	
	def __OnClose(self, event):
		self.root.destroy()
	
	def __CreateTransparent(self):
		''' Transparent Form parameters '''
		self.root.bind('<Button-1>', self.__OnClose)
		self.root.resizable(0,0)
		if platform.system() == 'Windows':
			self.root.overrideredirect(1)
		elif platform.system() == 'Linux':
			self.root.wm_attributes('-type', 'splash')
		self.root.lift()
		self.root.wm_attributes("-topmost", self.args.Topmost)
		self.root.after_idle(self.root.attributes,'-topmost', self.args.Topmost)
		self.root.wait_visibility(self.root)
	
	def __CreateStyle(self):
		''' Create Style elements on form '''
		self.style.configure('H.TLabel', background=self.args.BG,
							foreground=self.args.TitleFG,
							font=self.TitleFont,
							justify=tk.CENTER, borderwidth=0)
		self.style.configure('B.TLabel', 
							background=self.args.BG,
							foreground=self.args.BodyFG,
							font=self.BodyFont,
							justify=tk.CENTER,
							borderwidth=0)
		self.style.configure('I.TLabel', 
							background=self.args.BG,
							foreground=self.args.BodyFG,
							justify=tk.CENTER,
							borderwidth=0)
	
	def __CreateBtnClose(self):
		''' Create Button on Close '''
		closeIcon = ''
		if self.args.Style == FormStyle.Standart.value:
			if self.args.CloseIcon == 'default':
				closeIcon = Defaults.PREFIX.joinpath('exit_close_24x24.png')
			elif self.args.CloseIcon != 'None':
				closeIcon = pathlib.Path(str(self.args.CloseIcon)).resolve() if pathlib.Path(str(self.args.CloseIcon)).resolve().exists else ''
			else:
				closeIcon = ''
			if closeIcon != '':
				
				self.close_icon = Image.open(str(pathlib.Path(str(closeIcon)).resolve()))
				self.close_icon = self.close_icon.resize((tuple(map(int, self.args.ScaleClose.split(',')))), Image.LANCZOS)
				self.close_icon = ImageTk.PhotoImage(self.close_icon)
				
				self.btn1 = tk.Button(self.root, text="", justify=tk.CENTER,
								borderwidth=0,
								bg=self.args.BG,
								fg=self.args.TitleFG,
								highlightcolor='white',
								activebackground='white',
								highlightthickness = 0,
								image=self.close_icon,
								command=self.root.destroy)
			else:
				self.close_icon = 'None'
	
	def __CreateHeader(self):
		''' Create Header '''
		self.label_header = ttk.Label(self.root, text=self.args.Title, style='H.TLabel')
		self.label_header.bind('<Button-1>', self.__OnClose)

	def __CreateIcon(self):
		''' Crete Icon on forms (image) '''
		if self.args.icon != 'None':
			if pathlib.Path(str(self.args.icon)).resolve().exists():

				self.image = Image.open(str(pathlib.Path(str(self.args.icon)).resolve()))
				self.image = self.image.resize((tuple(map(int, self.args.scale.split(',')))), Image.LANCZOS)
				self.image = ImageTk.PhotoImage(self.image)
				
				self.label_image = ttk.Label(self.root, text="", style='I.TLabel')
				self.label_image.bind('<Button-1>', self.__OnClose)
				self.label_image.image = self.image
				self.label_image['image'] = self.label_image.image
			else:
				self.image = 'None'
	
	def __CreateText(self):
		''' Create Text notify '''
		self.label_text = ttk.Label(self.root, text=self.args.Message, style='B.TLabel')
		self.label_text.bind('<Button-1>', self.__OnClose)
	
	def __ElementPack(self):
		''' Elements send (pack, place or grid standart class method) to Form '''
		if self.args.Style == FormStyle.Standart.value:
			for c in range(3):
				self.root.columnconfigure(index=c, weight=1)
			for r in range(2):
				self.root.rowconfigure(index=r, weight=1)
			if self.args.icon != '':
				self.label_header.grid(row=0, column=0, columnspan=2, sticky='w', padx=(10, 0), pady=0)
			else:
				self.label_header.grid(row=0, column=0, columnspan=2, sticky='w', padx=(5, 0), pady=0)
			if self.close_icon != 'None':
				self.btn1.grid(row=0, column=2)
			if self.args.icon != 'None':
				if self.image != 'None':
					self.label_image.grid(row=1, column=0, padx=(10, 0), pady=(0, 5))
					self.label_text.grid(row=1, column=1, padx=(0, 0), pady=(0, 10), sticky='w')
				else:
					self.label_text.grid(row=1, column=0, padx=(11, 10), pady=(0, 15), sticky='w')
			else:
				self.label_text.grid(row=1, column=0, padx=(11, 10), pady=(0, 15), sticky='w')
		else:
			if self.args.icon != 'None':
				for c in range(2):
					self.root.columnconfigure(index=c, weight=1)
				for r in range(2):
					self.root.rowconfigure(index=r, weight=1)
				if self.image != 'None':
					self.label_image.grid(row=0, column=0, rowspan=2, sticky='w', padx=(10, 0), pady=(0, 0))
					self.label_header.grid(row=0, column=1, padx=(0, 10), pady=(0, 0), sticky='sw')
					self.label_text.grid(row=1, column=1, padx=(0, 10), pady=(0, 0), sticky='nw')
				else:
					self.label_header.grid(row=0, column=0, padx=(15, 10), pady=(0, 0), sticky='sw')
					self.label_text.grid(row=1, column=0, padx=(15, 10), pady=(0, 0), sticky='nw')
			else:
				for c in range(1):
					self.root.columnconfigure(index=c, weight=1)
				for r in range(2):
					self.root.rowconfigure(index=r, weight=1)
				self.label_header.grid(row=0, column=0, padx=(15, 10), pady=(0, 0), sticky='sw')
				self.label_text.grid(row=1, column=0, padx=(15, 10), pady=(0, 0), sticky='nw') # , ipadx=0, ipady=0
		
	def __CalcPosition(self):
		''' Calculate Position Left (x) '''
		if len(self.args.SocketFormPos.keys()) == 6:
			self.left, self.top = Defaults.CalcNewPosition(self.screen_width, self.screen_height, 
															self.args.SocketFormPos['position_x'], self.args.SocketFormPos['position_y'], 
															self.args.SocketFormPos['Width'], self.args.SocketFormPos['Height'], 
															self.args.SocketFormPos['Left'], self.args.SocketFormPos['Top'], self.args.distance)
															# scr_width scr_height pos_x pos_y width height left top
		else:
			self.left = Defaults.CalcPositionX(self.args.PosX, self.screen_width, self.width)
			self.top = Defaults.CalcPositionY(self.args.PosY, self.screen_height, self.height)
	
	def RelativePosition(self, x: int = 0, y: int = 0):
		''' Change relative coordinate position form on left (x) and top (y) '''
		self.left += x
		self.top += y
		self.root.geometry(f"+{self.left}+{self.top}")
		self.root.update_idletasks()
	
	def RealPosition(self, x: int, y: int):
		''' Change absolute coordinate position form on left (x) and top (y) '''		
		self.left = x
		self.top = y
		self.root.geometry(f"+{self.left}+{self.top}")
		self.root.update_idletasks()
	
	def __CreatePosition(self):
		''' Position Forms on Desktop '''
		self.screen_width = self.root.winfo_screenwidth()
		self.screen_height = self.root.winfo_screenheight()
		self.root.geometry()
		self.root.update_idletasks()
		form_size = self.root.geometry()
		self.width = tuple(map(int, form_size.split('+')[0].split('x')))[0] + 10
		self.height = tuple(map(int, form_size.split('+')[0].split('x')))[1] + 10
		self.root.geometry(f"{self.width}x{self.height}")
		self.root.update_idletasks()
		self.left = 0
		self.top = 0
		
		self.args.FormPos['position_x'] = self.args.PosX if type(self.args.PosX) == str else self.args.PosX.value
		self.args.FormPos['position_y'] = self.args.PosY if type(self.args.PosY) == str else self.args.PosY.value
		self.args.FormPos['Width'] = self.width
		self.args.FormPos['Height'] = self.height
		
		self.__CalcPosition()
		
		self.root.geometry(f"+{self.left}+{self.top}")
		self.root.update_idletasks()
		
		if self.args.MoveX != 0 or self.args.MoveY != 0:
			if self.args.Relative:
				self.RelativePosition(self.args.MoveX, self.args.MoveY)
			else:
				self.RealPosition(self.args.MoveX, self.args.MoveY)
		
		self.root.minsize(110, 70)
		self.root.maxsize(self.screen_width, self.screen_height)
		self.root.resizable(0,0)
		self.args.FormPos['Top'] = self.top
		self.args.FormPos['Left'] = self.left

class QueueManager(BaseManager):
	pass

class UserTimer:
	def __init__(self, link):
		self.link = link
		self.stop_timer = threading.Timer(1, lambda:self.link.stop_event.set())
	
	def start(self):
		print('Stop Server')
		self.stop_timer.start()

class ClientServer:
	
	DEBUG = Boolean()
	connected = Boolean()
	is_server = Boolean()
	data_out = Strings()
	port = 5007
	host = HostName()
	ServerPID = Integer()
	PID = SetPID()

	def __init__(self):
		self.is_server = False
		self.connected = False
		self.data_out = ''
		self.DEBUG = False	
		self.ServerPID = 0
	
	def TestConnected(self, address, port):
		s = socket.socket()
		self.connected = False
		try:
			s.connect((address, port))
			self.connected = True
			self.is_server = False
		except Exception as e:
			#print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
			self.connected = False
			self.is_server = True
		finally:
			s.close()
		if self.connected:
			self.is_server = False
		else:
			self.is_server = True

	def exit_handler(self, signum, frame):
		self.qmanager.shutdown()
		print(f"Exit {ProgName.full}...")
		sys.exit(0)

	def RunServer(self):
		self.smanager.serve_forever()

	def StopServer(self):
		if self.connected:
			self.qmanager.stop()

	def KillServer(self, socket_file):
		socketfile = pathlib.Path(str(socket_file)).resolve()
		if socketfile.exists():
			port_dict = Files.read_write_json(socketfile, 'r')
			temp_pid = 0
			if port_dict.get('pid', '') != '' and type(port_dict.get('pid', '')) == int:
				temp_pid = port_dict.get('pid', '')
			
			if self.ServerPID == temp_pid:
				if self.ServerPID != 0:
					if Files.check_pid(self.ServerPID):
						os.kill(self.ServerPID, signal.SIGTERM)
			else:
				if self.ServerPID != 0:
					if Files.check_pid(self.ServerPID):
						os.kill(self.ServerPID, signal.SIGTERM)
				if self.temp_pid != 0:
					if Files.check_pid(self.temp_pid):
						os.kill(self.temp_pid, signal.SIGTERM)
			self.save_server_pid(socketfile, True)
		else:
			if self.ServerPID != 0:
				if Files.check_pid(self.ServerPID):
					os.kill(self.ServerPID, signal.SIGTERM)

	def ClientConnect(self):
		self.connected = False
		try:
			self.qmanager.connect()
			self.connected = True
		except:
			self.connected = False
		if self.connected:
			self.task = self.qmanager.GetTasks()
			self.ServerPID = self.task.get(0)

	def ServerInit(self):
		self.smanager = self.qmanager.get_server()
		self.stop_timer = UserTimer(self.smanager) # threading.Timer(1, lambda:self.smanager.stop_event.set())
		QueueManager.register('stop', callable=lambda:self.stop_timer.start())
		self.task.put(self.PID)

	def ClientServerINIT(self):
		if self.is_server:
			signal.signal(signal.SIGTERM, self.exit_handler)
			self.task = tasks.Task()
			QueueManager.register('GetTasks', callable=lambda:self.task)
		else:
			QueueManager.register('GetTasks')
			QueueManager.register('stop')
		self.qmanager = QueueManager(address=(self.get_host(), self.get_port()), authkey=Defaults.access_key)

	def Client_Server(self):
		self.ClientServerINIT()
		if self.is_server:
			self.ServerInit()
		else:
			self.ClientConnect()

	def __str__(self):
		return self.data_out

	def __repr__(self):
		return f"{self.__class__.__name__}:\n\t" +\
				f"is_server: {self.is_server}\n\t" +\
				f"connected: {self.connected}\n\t" +\
				f"data_out: {self.data_out}\n\t" +\
				f"DEBUG: {self.DEBUG}\n\t" +\
				f"host: {self.host}\n\t" +\
				f"port: {self.port}\n\t"

	def set_free_port(self, socket_file):
		socketfile = pathlib.Path(str(socket_file)).resolve()
		if not socketfile.exists():
			socketfile.parent.mkdir(mode=0o755, parents=True,exist_ok=True)
			self.find_free_port()
			port_dict = {'port': self.get_port()}
			Files.read_write_json(socketfile, 'w', port_dict)
		else:
			port_dict = Files.read_write_json(socketfile, 'r')
			if port_dict.get('port', '') != '' and type(port_dict.get('port', '')) == int:
				self.set_port(port_dict.get('port', ''))
			if port_dict.get('pid', '') != '' and type(port_dict.get('pid', '')) == int:
				self.ServerPID = port_dict.get('pid', '')

	def save_server_pid(self, socket_file, isreset: bool = False):
		socketfile = pathlib.Path(str(socket_file)).resolve()
		if not socketfile.exists():
			socketfile.parent.mkdir(mode=0o755, parents=True,exist_ok=True)
			self.find_free_port()
			if not isreset:
				port_dict = {'port': self.get_port(), 'pid': self.PID}
			else:
				port_dict = {'port': self.get_port(), 'pid': 0}
			Files.read_write_json(socketfile, 'w', port_dict)
		else:
			port_dict = Files.read_write_json(socketfile, 'r')
			if not isreset:
				port_dict['pid'] = self.PID
			else:
				port_dict['pid'] = 0
			Files.read_write_json(socketfile, 'w', port_dict)
	
	@classmethod
	def find_free_port(cls):
		with socket.socket() as s:
			s.bind(('', 0))            # Bind to a free port provided by the host.
			cls.set_port(s.getsockname()[1])  # Return the port number assigned.
	
	@classmethod
	def get_host(cls):
		return cls.host
	
	@classmethod
	def get_port(cls):
		return cls.port
	
	@classmethod
	def set_port(cls, value):
		cls.port = value

def createParser(argv):
	
	dict_parser = dict()
	'''
	Кросс-платформенные графические уведомления и напоминания на рабочем столе на основе Tk/Tcl.
	Cross-platform graphical desktop notifications and reminders based on Tk/Tcl.
	'''
	parser = argparse.ArgumentParser(prog=ProgName.name, description=argv.Lang[argv.lng]['description'])
	parser.add_argument ('-V', '--version', action='version', version=f'{ProgName.name} {__version__}',  help=argv.Lang[argv.lng]['version'])
	parser.add_argument ('-info', '--info', action='store_true', default=False, help=argv.Lang[argv.lng]['info'])
	parser.add_argument("-lng", '--lng', choices=['eng', 'ru'], default='ru', help=argv.Lang[argv.lng]['lng'])
	if  platform.system() == 'Windows':
		parser.add_argument("-console", '--console', dest="console", metavar='CONSOLE', type=str, default='cmd.exe', help=argv.Lang[argv.lng]['console'])
	else:
		parser.add_argument("-console", '--console', dest="console", metavar='CONSOLE', type=str, default='sh', help=argv.Lang[argv.lng]['console'])
	parser.add_argument("-ontime", '--ontime', dest="ontime", metavar='ONTIME', type=int, default=5000, help=argv.Lang[argv.lng]['ontime'])
	parser.add_argument ('-notimer', '--notimer', action='store_false', default=True, help=argv.Lang[argv.lng]['notimer'])
	parser.add_argument('-style', choices=['standart', 'compact'], default='compact', help=argv.Lang[argv.lng]['style'])
	parser.add_argument("-distance", '--distance', dest="distance", metavar='DISTANCE', type=int, default=10, help=argv.Lang[argv.lng]['distance'])
	parser.add_argument("-alpha", '--alpha', dest="alpha", metavar='ALPHA', type=float, default=1.0, help=argv.Lang[argv.lng]['alpha'])
	dict_parser['parser'] = parser
	
	subparsers = parser.add_subparsers(title=argv.Lang[argv.lng]['sub_title'], description=argv.Lang[argv.lng]['sub_desc'], help=argv.Lang[argv.lng]['sub_help'])
	
	dict_parser['subparsers'] = subparsers

	if platform.system() == 'Linux':
		parser_systemd = subparsers.add_parser('systemd', help=argv.Lang[argv.lng]['systemd']['info'])
		
		parser_systemd.add_argument ('-create', '--create', action='store_true', default=False, help=argv.Lang[argv.lng]['systemd']['create'])
		parser_systemd.add_argument ('-delete', '--delete', action='store_true', default=False, help=argv.Lang[argv.lng]['systemd']['delete'])
		parser_systemd.add_argument ('-status', '--status', action='store_true', default=False, help=argv.Lang[argv.lng]['systemd']['status'])
		parser_systemd.add_argument ('-enable', '--enable', action='store_true', default=False, help=argv.Lang[argv.lng]['systemd']['enable'])
		parser_systemd.add_argument ('-disable', '--disable', action='store_true', default=False, help=argv.Lang[argv.lng]['systemd']['disable'])
		parser_systemd.add_argument ('-start', '--start', action='store_true', default=False, help=argv.Lang[argv.lng]['systemd']['start'])
		parser_systemd.add_argument ('-stop', '--stop', action='store_true', default=False, help=argv.Lang[argv.lng]['systemd']['stop'])
		parser_systemd.add_argument ('-reload', '--reload', action='store_true', default=False, help=argv.Lang[argv.lng]['systemd']['reload'])
		parser_systemd.set_defaults(onlist='systemd')
		
		dict_parser['parser_systemd'] = parser_systemd
	
	parser_daemon = subparsers.add_parser('daemon', help=argv.Lang[argv.lng]['daemon']['info'])
	
	parser_daemon.add_argument ('-start', '--start', action='store_true', default=False, help=argv.Lang[argv.lng]['daemon']['start'])
	parser_daemon.add_argument('-run', '--run', action='store_true', default=False, help=argparse.SUPPRESS)
	parser_daemon.add_argument ('-stop', '--stop', action='store_true', default=False, help=argv.Lang[argv.lng]['daemon']['stop'])
	parser_daemon.add_argument ('-restart', '--restart', action='store_true', default=False, help=argv.Lang[argv.lng]['daemon']['restart'])
	parser_daemon.add_argument ('-kill', '--kill', action='store_true', default=False, help=argv.Lang[argv.lng]['daemon']['kill'])
	parser_daemon.set_defaults(onlist='daemon')
	
	dict_parser['parser_daemon'] = parser_daemon
	
	group1 = parser.add_argument_group(argv.Lang[argv.lng]['title_group'], argv.Lang[argv.lng]['title_info'])
	group1.add_argument("-title", '--title', dest="title", metavar='TITLE', type=str, default='Apps', help=argv.Lang[argv.lng]['title'])
	group1.add_argument("-tfamily", '--tfamily', dest="tfamily", metavar='TFAMILY', type=str, default='Arial', help=argv.Lang[argv.lng]['tfamily'])
	group1.add_argument("-tsize", '--tsize', dest="tsize", metavar='TSIZE', type=int, default=12, help=argv.Lang[argv.lng]['tsize'])
	group1.add_argument('-tweight', choices=['bold', 'normal'], default='bold', help=argv.Lang[argv.lng]['tweight'])
	group1.add_argument("-tund", '--tund', dest="tund", metavar='TUND', type=int, default=0, help=argv.Lang[argv.lng]['tund'])
	group1.add_argument('-tslant', choices=['roman', 'Italic'], default='roman', help=argv.Lang[argv.lng]['tslant'])
	group1.add_argument("-tstrike", '--tstrike', dest="tstrike", metavar='TSTRIKE', type=int, default=0, help=argv.Lang[argv.lng]['tstrike'])
	group1.add_argument("-tcolor", '--tcolor', dest="tcolor", metavar='TCOLOR', type=str, default='black', help=argv.Lang[argv.lng]['tcolor'])
	dict_parser['group1'] = group1
	
	group2 = parser.add_argument_group(argv.Lang[argv.lng]['mess_group'], argv.Lang[argv.lng]['mess_info'])
	group2.add_argument("-text", '--text', dest="text", metavar='TEXT', type=str, default='Info', help=argv.Lang[argv.lng]['text'])
	group2.add_argument("-bg", '--bg', dest="bg", metavar='BG', type=str, default='#FFFADD', help=argv.Lang[argv.lng]['bg'])
	group2.add_argument("-bcolor", '--bcolor', dest="bcolor", metavar='BCOLOR', type=str, default='black', help=argv.Lang[argv.lng]['bcolor'])
	group2.add_argument("-bfamily", '--bfamily', dest="bfamily", metavar='BFAMILY', type=str, default='Arial', help=argv.Lang[argv.lng]['bfamily'])
	group2.add_argument("-bsize", '--bsize', dest="bsize", metavar='BSIZE', type=int, default=12, help=argv.Lang[argv.lng]['bsize'])
	group2.add_argument('-bweight', choices=['bold', 'normal'], default='normal', help=argv.Lang[argv.lng]['bweight'])
	group2.add_argument("-bund", '--bund', dest="bund", metavar='BUND', type=int, default=0, help=argv.Lang[argv.lng]['bund'])
	group2.add_argument('-bslant', choices=['roman', 'Italic'], default='roman', help=argv.Lang[argv.lng]['bslant'])
	group2.add_argument("-bstrike", '--bstrike', dest="bstrike", metavar='BSTRIKE', type=int, default=0, help=argv.Lang[argv.lng]['bstrike'])
	dict_parser['group2'] = group2
	
	group3 = parser.add_argument_group(argv.Lang[argv.lng]['icon_group'], argv.Lang[argv.lng]['icon_info'])
	group3.add_argument("-icon", '--icon', dest="icon", metavar='ICON', type=str, default='None', help=argv.Lang[argv.lng]['icon'])
	group3.add_argument("-close", '--close', dest="close", metavar='CLOSE', type=str, default='default', help=argv.Lang[argv.lng]['close'])
	group3.add_argument("-scale", '--scale', dest="scale", metavar='SCALE', type=str, default='48,48', help=argv.Lang[argv.lng]['scale'])
	group3.add_argument("-clscale", '--clscale', dest="clscale", metavar='CLSCALE', type=str, default='24,24', help=argv.Lang[argv.lng]['clscale'])
	dict_parser['group3'] = group3
	
	group4 = parser.add_argument_group(argv.Lang[argv.lng]['offset_group'], argv.Lang[argv.lng]['offset_info'])
	group4.add_argument('-posx', choices=['left', 'center', 'right'], default='right', help=argv.Lang[argv.lng]['posx'])
	group4.add_argument('-posy', choices=['top', 'center', 'bottom'], default='top', help=argv.Lang[argv.lng]['posy'])
	group4.add_argument("-x", '--x', dest="x", metavar='X', type=int, default=0, help=argv.Lang[argv.lng]['x'])
	group4.add_argument("-y", '--y', dest="y", metavar='Y', type=int, default=0, help=argv.Lang[argv.lng]['y'])
	group4.add_argument ('-relative', '--relative', action='store_false', default=True, help=argv.Lang[argv.lng]['relative'])
	group4.add_argument ('-topmost', '--topmost', action='store_true', default=False, help=argv.Lang[argv.lng]['topmost'])
	dict_parser['group4'] = group4
	
	parser_options = subparsers.add_parser('config', help=argv.Lang[argv.lng]['config']['info'])
	parser_options.add_argument ('-show', '--show', action='store_true', default=False, help=argv.Lang[argv.lng]['config']['show'])
	parser_options.add_argument ('-dirs', '--dirs', action='store_true', default=False, help=argv.Lang[argv.lng]['config']['dirs'])
	#parser_options.add_argument ('-load', '--load', action='store_true', default=False, help=argv.Lang[argv.lng]['config']['load'])
	parser_options.add_argument ('-save', '--save', action='store_true', default=False, help=argv.Lang[argv.lng]['config']['save'])
	parser_options.add_argument ('-reset', '--reset', action='store_true', default=False, help=argv.Lang[argv.lng]['config']['reset'])
	parser_options.add_argument("-theme", '--theme', dest="theme", metavar='THEME', type=str, default='', help=argv.Lang[argv.lng]['config']['theme'])
	parser_options.add_argument("-output", '--output', dest="output", metavar='OUTPUT', type=str, default='', help=argv.Lang[argv.lng]['config']['output'])
	parser_options.set_defaults(onlist='config')
	dict_parser['parser_options'] = parser_options
	
	return dict_parser

def empty(argv):
	pass

def systemd_process(argv):
	if argv.create:
		SystemdConfig.create_service()
		sys.exit(0)
	if argv.delete:
		SystemdConfig.remove_service(argv.console)
		sys.exit(0)
	if SystemdConfig.systemd_question(argv) != 'empty':
		service, err = SystemdConfig.control(argv.console, SystemdConfig.systemd_question(argv))
		if service != '':
			print(service)
		if err != '':
			print('Error:\n', err)
		sys.exit(0)
	else:
		argv.parser_dict['parser_systemd'].parse_args(['-h'])
		sys.exit(0)

def daemon_process(argv):
	def run_script_shell():
		python = str(pathlib.Path(str(sys.executable)).resolve())
		script = str(pathlib.Path(sys.argv[0]).resolve())
		cmd = []
		if  platform.system() == 'Windows':
			if python == script:
				cmd = ['start', '/b', script, 'daemon', '-run']
			else:
				cmd = ['start', '/b', python, script, 'daemon', '-run']
		else:
			if python == script:
				cmd = [script, 'daemon', '-run', '&']
			else:
				cmd = [python, script, 'daemon', '-run', '&']
		result = SHELL.shell_run(cmd)
	if argv.run and argv.client_server.is_server:
		argv.client_server.Client_Server()
		argv.client_server.save_server_pid(Files.socket_file, False)
		argv.client_server.RunServer()
		argv.client_server.save_server_pid(Files.socket_file, True)
		sys.exit(0)
	if argv.start and argv.client_server.is_server:
		run_script_shell()
		sys.exit(0)
	if argv.stop and not argv.client_server.is_server:
		argv.client_server.Client_Server()
		argv.client_server.StopServer()
		argv.client_server.save_server_pid(Files.socket_file, True)
		sys.exit(0)
	if argv.restart and not argv.client_server.is_server:
		argv.client_server.Client_Server()
		argv.client_server.StopServer()
		argv.client_server.save_server_pid(Files.socket_file, True)
		run_script_shell()
		sys.exit(0)
	if argv.kill and not argv.client_server.is_server:
		argv.client_server.Client_Server()
		argv.client_server.KillServer(Files.socket_file)
		sys.exit(0)
	argv.parser_dict['parser_daemon'].parse_args(['-h'])
	sys.exit(0)

def config_process(argv):
	if argv.show:
		for item in Files.ThemeDir.glob('*.json'):
			print(str(item.name))
		sys.exit(0)
	if argv.dirs:
		print(str(Files.ThemeDir))
		sys.exit(0)
	#if argv.load:
	#	argv.LoadConfig()
	if argv.reset:
		argv.CreateDefaultConfig()
	if argv.save:
		argv.SaveConfig()
	#if not argv.reset and not argv.save:
	#	argv.parser_dict['parser_options'].parse_args(['-h'])
	sys.exit(0)

def main(*argv):
	
	args = Arguments()
	parser_dict = createParser(args)
	
	if len(argv) > 0:
		parser_dict['parser'].parse_args(args=argv, namespace=Arguments)
	else:
		parser_dict['parser'].parse_args(namespace=Arguments)
	
	args.FixArgs()
	
	args.parser_dict = parser_dict
	
	if args.Theme != '':
			args.ApplyTheme()
	
	if args.info:
		print(Author.Info)
		sys.exit(0)
	
	args.client_server = Files.CreateClientServer()
	args.client_server.TestConnected(args.client_server.get_host(), args.client_server.get_port())
	
	func = {
				'systemd': systemd_process,
				'daemon': daemon_process,
				'config': config_process
			}.get(args.onlist, empty)(args)
	
	args.client_server.TestConnected(args.client_server.get_host(), args.client_server.get_port())
	
	if not args.client_server.is_server:
		args.client_server.Client_Server()
		
		task_list = args.client_server.task.copy()
		args.SocketFormPos = args.Search_Socket_Pos(task_list)
		
		notification = Notify(args)
		
		args.client_server.task.put(notification.args.FormPos)	
		
		notification.send()
		
		args.client_server.task.remove(notification.args.FormPos)
	
	#if args.onlist == None:
	#	parser_dict['parser'].parse_args(['-h'])

if __name__ == '__main__':
	main()

