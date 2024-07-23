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

__author__ = 'Mikhail Artamonov'
__description__ = 'Cross-platform graphical desktop notifications and reminders based on Tk/Tcl.'
__progname__ = str(pathlib.Path(sys.argv[0]).resolve().name)
__copyright__ = f"© The \"{__progname__}\". Copyright  by 2024."
__credits__ = ["Mikhail Artamonov"]
__license__ = "GPL3"
__version__ = "1.0.0"
__maintainer__ = "Mikhail Artamonov"
__status__ = "Production"
__date__ = '11.10.2022'
__modifed__ = '22.07.2024'

class Prog_Name:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return str(pathlib.Path(__progname__).name).split('.')[0]

class Full_Prog:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return str(pathlib.Path(sys.argv[0]).resolve())

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

class SystemdConfig:
	
	config = SystemdText()
	
	def __repr__(self):
		return f"{self.__class__}: {self.config}"
	
	def __str__(self):
		return f"{self.config}"
	
	def __call__(self):
		return f"{self.config}"

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

class Meta(type):
	
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@property
	def access_key(cls):
		return Texts.StrToBase(Texts.Access)
	
	@property
	def SockFileName(cls):
		return f"pynotifyr.sock"
	
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
	def dark_theme(cls):
		return cls.ThemeDir.joinpath(Defaults.DarkThemeName)

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
		self.except_list.append('Reset')
		self.except_list.append('ApplyTheme')
		self.except_list.append('SaveTheme')
		self.except_list.append('CreateDefaultConfig')
		self.except_list.append('save')
		self.except_list.append('load')
		self.except_list.append('reset')
		self.except_list.append('output')
		self.except_list.append('FormPos')
		self.except_list.append('TempPos')
		self.except_list.append('SocketFormPos')
		self.except_list.append('ThemeDict')
		self.except_list.append('isTheme')
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
		self.scale = args[20] if len(args) >= 21 else kwargs.get('scale', '1,1')
		self.PosX = args[21] if len(args) >= 22 else kwargs.get('PosX', 'right')
		self.PosY = args[22] if len(args) >= 23 else kwargs.get('PosY', 'top')
		self.Alpha = args[23] if len(args) >= 24 else kwargs.get('Alpha', 1.0)
		self.MoveX = args[24] if len(args) >= 25 else kwargs.get('MoveX', 0)
		self.MoveY = args[25] if len(args) >= 26 else kwargs.get('MoveY', 0)
		self.Relative = args[26] if len(args) >= 27 else kwargs.get('Relative', True)
		self.Topmost = args[27] if len(args) >= 28 else kwargs.get('Topmost', False)
		self.save = args[28] if len(args) >= 29 else kwargs.get('save', False)
		self.load = args[29] if len(args) >= 30 else kwargs.get('load', False)
		self.reset = args[30] if len(args) >= 31 else kwargs.get('reset', False)
		self.CloseIcon = args[31] if len(args) >= 32 else kwargs.get('CloseIcon', 'default')
		self.Theme = args[32] if len(args) >= 33 else kwargs.get('Theme', '')
		self.isTheme = args[33] if len(args) >= 34 else kwargs.get('isTheme', False)
		self.output = args[34] if len(args) >= 35 else kwargs.get('output', '')
		self.Style = args[35] if len(args) >= 36 else kwargs.get('Style', 'standart')
		self.ScaleClose = args[36] if len(args) >= 37 else kwargs.get('ScaleClose', '1,1')
		self.distance = args[37] if len(args) >= 38 else kwargs.get('distance', 10)
		self.FormPos = dict()
		self.SocketFormPos = dict()
		self.TempPos = dict()
		self.ThemeDict = dict()
		temp_theme = f"{self.Theme}"
		if Files.ConfigFileName.exists():
			config = configparser.ConfigParser()
			Files.read_write_config(str(Files.ConfigFileName), 'r', config)
			self.Theme = config['Main']['Theme']
			self.ApplyTheme()
			self.Theme = f"{temp_theme}"
		if self.Theme != '':
			self.ApplyTheme()
	
	def CreateDefaultConfig(self):
		dark_theme = Files.dark_theme
		light_theme = Files.light_theme
		
		self.icon = pathlib.Path(str(self.icon)).resolve() if self.icon != '' and self.icon != 'None' else self.icon
		self.CloseIcon = pathlib.Path(str(self.CloseIcon)).resolve() if self.CloseIcon != '' and self.CloseIcon != 'None' else self.CloseIcon
		
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
		self.scale = '5,5'
		self.ScaleClose = '1,1'
		self.PosX = 'right'
		self.PosY = 'top'
		self.MoveX = 0
		self.MoveY = 0
		self.OnTime = 5000
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
		
		self.output = dark_theme
		
		self.SaveTheme()
				
		self.BG = '#FFFADD'
		self.TitleFG = 'black'
		self.BodyFG = 'black'
		self.Alpha = 0.8
		
		self.output = light_theme
		
		self.SaveTheme()
		
		config = configparser.ConfigParser()
		config['Main'] = {'Theme': f"{light_theme}"}
		
		Files.read_write_config(str(Files.ConfigFileName), 'w', config)
		
		for k, v in temp_theme.items():
			self.__dict__[k] = v
		
		self.icon = pathlib.Path(str(self.icon)).resolve() if self.icon != '' and self.icon != 'None' else self.icon
		self.CloseIcon = pathlib.Path(str(self.CloseIcon)).resolve() if self.CloseIcon != '' and self.CloseIcon != 'None' else self.CloseIcon
	
	def ApplyTheme(self):
		self.Theme = pathlib.Path(str(self.Theme)).resolve()
		if self.Theme.exists():
			self.ThemeDict = Files.read_write_json(self.Theme, 'r')
			for k in self.ThemeDict.keys():
				if self.ThemeDict.get(k, '') != '':
					self.__dict__[k] = self.ThemeDict.get(k, '')
	
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
		self.scale = '1,1'
		self.PosX = 'right'
		self.PosY = 'top'
		self.Alpha = 1.0
		self.MoveX = 0
		self.MoveY = 0
		self.Relative = True
		self.Topmost = False
		self.save = False
		self.load = False
		self.reset = False
		self.CloseIcon = 'default'
		self.Theme = ''
		self.isTheme = False
		self.output = ''
		self.Style = 'standart'
		self.ScaleClose = '1,1'
		self.distance = 10
		self.FormPos.clear()
		self.TempPos.clear()
		self.SocketFormPos.clear()
		self.ThemeDict.clear()
	
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
				self.close_icon = tk.PhotoImage(file = closeIcon)
				self.close_icon = self.close_icon.subsample(*tuple(map(int, self.args.ScaleClose.split(','))))
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
				self.image = tk.PhotoImage(file=pathlib.Path(str(self.args.icon)).resolve())
				self.image = self.image.subsample(*tuple(map(int, self.args.scale.split(','))))
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
	
	def CalcNewPosition(self):
		self.args.TempPos.clear()
		if len(self.args.SocketFormPos.keys()) == 6:
			self.args.TempPos['Left'], self.args.TempPos['Top'] = Defaults.CalcNewPosition(self.screen_width, self.screen_height, 
																self.args.SocketFormPos['position_x'], self.args.SocketFormPos['position_y'], 
																self.args.SocketFormPos['Width'], self.args.SocketFormPos['Height'], 
																self.args.SocketFormPos['Left'], self.args.SocketFormPos['Top'], self.args.distance)
																# scr_width scr_height pos_x pos_y width height left top
			if self.args.MoveX != 0 or self.args.MoveY != 0:
				if self.args.Relative:
					self.args.TempPos['Left'] = self.args.TempPos['Left'] + self.args.MoveX
					self.args.TempPos['Top'] = self.args.TempPos['Top'] + self.args.MoveY
				else:
					self.args.TempPos['Left'] = self.args.MoveX
					self.args.TempPos['Top'] = self.args.MoveY
			self.args.TempPos['position_x'] = self.args.PosX if type(self.args.PosX) == str else self.args.PosX.value
			self.args.TempPos['position_y'] = self.args.PosY if type(self.args.PosY) == str else self.args.PosY.value
			self.args.TempPos['Width'] = self.width
			self.args.TempPos['Height'] = self.height
	
	def UsePosition(self):
		if len(self.args.SocketFormPos.keys()) == 6:
			self.args.FormPos['position_x'] = self.args.TempPos['position_x']
			self.args.FormPos['position_y'] = self.args.TempPos['position_y']
			self.args.FormPos['Top'] = self.args.TempPos['Top']
			self.args.FormPos['Left'] = self.args.TempPos['Left']
			self.left = self.args.TempPos['Left']
			self.top = self.args.TempPos['Top']
			self.root.geometry(f"+{self.left}+{self.top}")
			self.root.update_idletasks()
	
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
	
def main():
	'''
	args = Arguments(icon='./info.png', scale='3,3', Title='Apps!', Message='Mesages to text output information!', OnTime=5000,
	#args = Arguments(icon='None', scale='3,3', Title='Apps!', Message='Mesages to text output information!', OnTime=5000,
					PosX=PositionX.Right.value, PosY = PositionY.Bottom.value, isTimer = False, Topmost = False, 
					Style = FormStyle.Standart.value, MoveY = -40
					) # Theme = './theme/light.json'
	#args = Arguments(Theme = './theme/dark.json')
	
	#args.CloseIcon = Defaults.PREFIX.joinpath('exit_close_24x24.png')
	args.CloseIcon = './exit_close_24x24.png'
	dark_theme = {'TitleFG': 'white', 'BodyBG': '#303030', 'BodyFG': 'white', 'Alpha': 0.9}
	light_theme = {'TitleFG': 'blue', 'BodyBG': '#FFFADD', 'BodyFG': 'black', 'Alpha': 0.9}
	theme = light_theme	
	args.BG = theme['BodyBG']
	args.TitleFG = theme['TitleFG']
	args.BodyFG = theme['BodyFG']
	args.Alpha = theme['Alpha']
	args.TFSize = 12
	args.BFSize = 12
	#args.output = './example.json'
	#if args.output != '':
	#	args.SaveTheme()
	#args.Theme = './example.json'
	#args.ApplyTheme()
	#args = Arguments(icon='./info.png', scale='3,3', Title='Apps!', Message='Mesages to text output information!', PosX=PositionX.Right.value, PosY = PositionY.Bottom.value, MoveX = 0, MoveY = -40)
	
	#args.SocketFormPos.clear()
	'''
	'''
	#args = Arguments()
	notification = Notify(args)
	notification.send()
	print(notification.args.SocketFormPos)
	'''
	'''
	args.SocketFormPos = {
							'position_x': PositionX.Right.value,
							'position_y': PositionY.Bottom.value,
							'Width': 337,
							'Height': 86,
							'Left': 1008,
							'Top': 652
						}
	'''
	'''
	client_server = ClientServer()
	client_server.TestConnected(client_server.get_host(), client_server.get_port())
	client_server.Client_Server()
	if client_server.is_server:
		client_server.RunServer()
	else:
		print('server_pid:', client_server.ServerPID, 'client_pid:', client_server.PID)
		client_server.task.put('hello')
		print(client_server.task.qsize())
		if not client_server.task.empty():
			print(client_server.task.get())
			client_server.task.task_done()
		else:
			print('Queue is empty!')
		print(client_server.task.qsize())
		#client_server.StopServer()
		if Files.check_pid(client_server.ServerPID):
			os.kill(client_server.ServerPID, signal.SIGTERM)
	'''
	pass

if __name__ == '__main__':
	main()

