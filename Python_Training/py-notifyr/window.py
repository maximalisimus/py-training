#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import json
import configparser
import argparse
import tkinter as tk
from enum import Enum
import threading
from os import getpid
import time

env_event = threading.Event()
worker_event = threading.Event()
screen_width = 0
screen_height = 0
position_x = 0
position_y = 0
Top = 0
Left = 0
Width = 0
Height = 0

class NoValue(Enum):

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class Weight(NoValue):
	normal = 'normal'
	bold = 'bold'
	
	@classmethod
	def GetWeightValue(cls, weight: str):
		for x in cls:
			if weight == x.value:
				return x
		return None

	@classmethod
	def GetWeightName(cls, pos):
		for x in cls:
			if os == x:
				return x
		return None

class PositionX(NoValue):
	Left = 'left'
	Right = 'right'
	Center = 'center'
	
	@classmethod
	def GetPosValue(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

	@classmethod
	def GetPosName(cls, pos):
		for x in cls:
			if os == x:
				return x
		return None

class PositionY(NoValue):
	Top = 'top'
	Center = 'center'
	Bottom = 'Bottom'

	@classmethod
	def GetPosValue(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

	@classmethod
	def GetPosName(cls, pos):
		for x in cls:
			if os == x:
				return x
		return None

class TypePositionMove(NoValue):
	Relative = 'relative'
	Real = 'real'
	
	@classmethod
	def GetTypePosValue(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

	@classmethod
	def GetTypePosName(cls, pos):
		for x in cls:
			if os == x:
				return x
		return None

class Defaults:
	
	PREFIX = pathlib.Path(sys.argv[0]).resolve().parent
	config_file = PREFIX.joinpath('config.ini').resolve()

	@staticmethod
	def CalcPositionX(pos_x: PositionX, scr_width: int, width: int):
		''' Calculate Position Left (x) '''
		if pos_x == PositionX.Left:
			calc_x = 15
		elif pos_x == PositionX.Center:
			calc_x = int(scr_width/2) - int(width/2)
		else:
			calc_x = scr_width - width - 15
		return calc_x

	@staticmethod
	def CalcPositionY(pos_y: PositionY, scr_height: int, height: int):
		''' Calculate Position Top (y) '''
		if pos_y == PositionY.Top:
			calc_y = 15
		elif pos_y == PositionY.Center:
			calc_y =  int(scr_height/2) - int(height/2)
		else:
			calc_y = scr_height - height - 30
		return calc_y

class Arguments:
	
	__slots__ = 'title text ontime icon fonts fgcolor bgcolor scale posx posy alpha movex movey typepos istimer'.split()
	
	def __init__(self, *args, **kwargs):
		self.title = args[0] if len(args) >= 1 else kwargs.get('title', 'Apps')
		self.text = args[1] if len(args) >= 2 else kwargs.get('text', 'Ok!')
		self.ontime = args[2] if len(args) >= 3 else kwargs.get('ontime', 10000)
		self.icon = pathlib.Path(args[3]).resolve() if len(args) >= 4 else kwargs.get('icon', '')
		self.fonts = list(str(args[4]).split(',')) if len(args) >= 5 else list(str(kwargs.get('fonts','Arial,14,normal')).split(','))
		self.fonts[1] = int(self.fonts[1])
		self.fonts[2] = Weight.GetWeightValue(self.fonts[2])
		self.fonts = tuple(self.fonts)
		self.fgcolor = args[5] if len(args) >= 6 else kwargs.get('fgcolor', 'black')
		self.bgcolor = args[6] if len(args) >= 7 else kwargs.get('bgcolor', '#FFFADD')
		self.scale = tuple(map(int, str(args[7]).split(',')))  if len(args) >= 8 else tuple(map(int, str(kwargs.get('scale', '1,1')).split(',')))
		self.posx = PositionX.GetPosValue(args[[8]]) if len(args) >= 9 else PositionX.GetPosValue(kwargs.get('posx', 'right'))
		self.posy = PositionY.GetPosValue(args[[9]]) if len(args) >= 10 else PositionY.GetPosValue(kwargs.get('posy', 'top'))
		self.alpha = args[10] if len(args) >= 11 else kwargs.get('alpha', 1.0)
		self.movex = args[11] if len(args) >= 12 else kwargs.get('movex', 0)
		self.movey = args[12] if len(args) >= 13 else kwargs.get('movey', 0)
		self.typepos = TypePositionMove.GetTypePosValue(args[13]) if len(args) >= 14 else TypePositionMove.GetTypePosValue(kwargs.get('typepos', 'relative'))
		self.istimer = args[14] if len(args) >= 15 else kwargs.get('istimer', True)
	
	def __getattr__(self, attrname):
		return None
	
	def __repr__(self):
		return f"{self.__class__}:" + \
				f"\n\tTitle: {self.title}" + \
				f"\n\tText: {self.text}" + \
				f",\n\tTime: {self.ontime} ms, isTimer: {self.istimer}," + \
				f",\n\tIcon: {self.icon if self.icon != '' else None}," + \
				f"\n\tFonts: {self.fonts}," + \
				f"\n\tFG Color: {self.fgcolor}, " + \
				f"BG Color: {self.bgcolor}, " + \
				f"\n\tScale: {self.scale}," + \
				f"\n\tPos X: {self.posx}, Pos Y: {self.posy}," + \
				f"\n\tAlpha: {self.alpha}," + \
				f"\n\tMove X: {self.movex}, Move Y: {self.movey}, Type Position Move: {self.typepos}"

class Window:
	
	def __init__(self, on_args: Arguments = Arguments()):
		''' Function init tkinter Apps '''
		self.args = on_args
		self.root = tk.Tk()
		
		# Window Functions builds
		self.__CreateTitle()
		self.__CreateTransparent()
		self.__CreateBtnClose()
		self.__CreateHeader()
		self.__CreateIcon()
		self.__CreateText()
		self.__ElementPack()
		self.__CreatePosition()
		
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
			self.root.after(self.args.ontime, self.update_clock)
	
	def __FormTimer_Init(self):
		''' Timer on destroy form parameters and functions '''
		self.timer_flag = True
		self.on_time = self.args.on_time
		self.counter = 0.1
		self.count = self.args.alpha
	
	def on_enter(self, event):
		''' Form focused '''
		self.root.attributes('-alpha', 1.0)
	
	def on_leave(self, enter):
		''' Form not focused '''
		self.root.attributes('-alpha', self.count)
	
	def Run(self):
		''' Global Form LOOP - visibility '''
		if self.args.istimer:
			self.update_clock()
		self.root.mainloop()
	
	def __CreateTitle(self):
		''' TKinter Title '''
		self.root.title(self.args.title)
		self.root.configure(bg=self.args.bgcolor)
	
	def __CreateTransparent(self):
		''' Transparent Form parameters '''
		self.root.resizable(0,0)
		self.root.overrideredirect(1)
		self.root.wm_attributes("-topmost", 1)
		self.root.wait_visibility(self.root)
	
	def __CreateBtnClose(self):
		''' Button on Close '''
		self.close_icon = tk.PhotoImage(file = Defaults.PREFIX.joinpath('close-icon.png'))
		self.close_icon = self.close_icon.subsample(1, 1)
		self.btn1 = tk.Button(self.root, text="", justify=tk.CENTER,
						borderwidth=0,
						bg=self.args.bgcolor,
						fg=self.args.fgcolor,
						highlightcolor='white',
						activebackground='white',
						highlightthickness = 0,
						image=self.close_icon,
						command=self.root.destroy
						)
	
	def __CreateHeader(self):
		''' Header '''
		self.label_3 = tk.Label(self.root, text=self.args.title,
							bg=self.args.bgcolor,
							fg=self.args.fgcolor,
							font=(self.args.fonts[0], self.args.fonts[1], 'bold'),
							justify=tk.CENTER,
							padx=10,
							pady=0
							)

	def __CreateIcon(self):
		''' Icon on forms (image) '''
		self.image = tk.PhotoImage(file=self.args.icon)
		self.image = self.image.subsample(*self.args.scale)
		self.label_1 = tk.Label(self.root, text=f"",
							bg=self.args.bgcolor,
							fg=self.args.fgcolor,
							font=(self.args.fonts[0], self.args.fonts[1], self.args.fonts[2].value),
							justify=tk.CENTER
							)
		self.label_1.image = self.image
		self.label_1['image'] = self.label_1.image
	
	def __CreateText(self):
		''' Text notify '''
		if self.args.icon != '':
			self.label_2 = tk.Label(self.root, text=self.args.text,
								bg=self.args.bgcolor,
								fg=self.args.fgcolor,
								font=(self.args.fonts[0], self.args.fonts[1], self.args.fonts[2]),
								justify=tk.CENTER
								)
		else:
			self.label_2 = tk.Label(self.root, text=self.args.text,
								bg=self.args.bgcolor,
								fg=self.args.fgcolor,
								font=(self.args.fonts[0], self.args.fonts[1], self.args.fonts[2]),
								justify=tk.CENTER,
								padx=5,
								pady=0
								)
	
	def __ElementPack(self):
		''' Elements send to Form '''
		self.label_3.grid(row=0, column=0)
		self.btn1.place(relx=0.915, rely=0.0)
		#self.btn1.grid(row=0, column=2)
		if self.args.icon != '':
			self.label_1.grid(row=1, column=0)
			self.label_2.grid(row=1, column=1)
		else:
			self.label_2.grid(row=1, column=0)
			self.label_2.place(relx=0.0, rely=0.5)
	
	def __CalcPosition(self):
		''' Calculate Position Left (x) '''
		self.left = Defaults.CalcPositionX(self.args.posx, self.screen_width, self.width)
		self.top = Defaults.CalcPositionY(self.args.posy, self.screen_height, self.height)
	
	def RelativePosition(self, x: int = 0, y: int = 0):
		''' Change new position form '''
		self.left += x
		self.top += y
		self.root.geometry(f"+{self.left}+{self.top}")
		self.root.update_idletasks()
	
	def RealPosition(self, x: int, y: int):
		self.left = x
		self.top = y
		self.root.geometry(f"+{self.left}+{self.top}")
		self.root.update_idletasks()
	
	def __CreatePosition(self):
		'''
			Position Forms on Desktop: pos_x = Desktop.width - Form.Width - left; pos_y = 15 - top 
			and Window size
		'''
		self.screen_width = self.root.winfo_screenwidth()
		self.screen_height = self.root.winfo_screenheight()
		self.root.geometry()
		self.root.update_idletasks()
		form_size = self.root.geometry()
		self.width = tuple(map(int, form_size.split('+')[0].split('x')))[0] + 10
		self.height = tuple(map(int, form_size.split('+')[0].split('x')))[1] + 10
		self.root.geometry(f"{self.width}x{self.height}")
		self.left = 0
		self.top = 0
		
		self.__CalcPosition()
		
		self.root.geometry(f"+{self.left}+{self.top}")
		self.root.update_idletasks()
		
		if self.args.movex != 0 or self.args.movey != 0:
			if self.args.typepos == TypePositionMove.Relative:
				self.RelativePosition(self.args.movex, self.args.movey)
			else:
				self.RealPosition(self.args.movex, self.args.movey)
		
		self.root.minsize(110, 70)
		self.root.maxsize(self.screen_width, self.screen_height)
		self.root.resizable(0,0)
		global screen_width
		global screen_height
		global position_x
		global position_y
		global Width
		global Height
		global Top
		global Left
		screen_width = self.screen_width
		screen_height = self.screen_height
		position_x = self.args.posx
		position_y = self.args.posy
		Top = self.top
		Left = self.left
		Width = self.width
		Height = self.height

class Files:
	
	@staticmethod
	def WriteJson(data_json: dict, file_json: str = 'object.json'):
		with open(pathlib.Path(file_json).resolve(), "w") as fp:
			json.dump(data_json, fp, indent=2)

	@staticmethod
	def ReadJson(file_json: str = 'object.json') -> dict:
		data = ''
		with open(pathlib.Path(file_json).resolve(), "r") as fp:
			data = json.load(fp)
		return data

	@staticmethod
	def GetFileSuffix(List_Files, suffixes: str):
		if List_Files != None:
			for x in List_Files:
				if suffixes == pathlib.Path(x).suffix:
					return pathlib.Path(x).resolve()
		return None

def main():
	args = Arguments(icon='test1.png', scale='2,2', title='Messages!', text='Mesages to text output information!', ontime=5000,
					posx=PositionX.Right.value, posy = PositionY.Top.value
					) # typepos = TypePositionMove.Relative.value posx=PositionX.Right.value, posy = PositionY.Top.value
	win = Window(args)
	# For Windows Bottom EditPosition
	#win.EditPosition(0, -10)
	#print(win.args.width, win.args.height, win.args.left, win.args.top)
	#win.EditPosition(-422, 204)
	#print(win.args.width, win.args.height, win.args.left, win.args.top)
	'''
	global screen_width
	global screen_height
	global position_x
	global position_y
	global Width
	global Height
	global Top
	global Left
	print(f"screen_width = {screen_width}, screen_height = {screen_height}")
	print(f"position_x = {position_x}, position_y = {position_y}")
	print(f"Width = {Width}, Height = {Height}, Left = {Left}, Top = {Top}")
	data = {
			'screen_width': 1366,
			'screen_height': 768,
			'position_x': PositionX.Right.value,
			'position_y': PositionY.Top.value,
			'Width': 412,
			'Height': 92,
			'Left': 939,
			'Top': 15
			}
	'''
	#win.RelativePosition(0,102)
	#win.RealPosition(0,0)
	win.Run()
	pass

if __name__ == '__main__':
	main()
