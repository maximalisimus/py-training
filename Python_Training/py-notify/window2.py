#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import json
import configparser
import argparse
import tkinter as tk
from tkinter import font as fnt
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
	''' Base Enum class elements '''

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class Weight(NoValue):
	''' Weight parameter fonts '''
	Normal = 'normal'
	Bold = 'bold'
	
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

class Defaults:
	
	PREFIX = pathlib.Path(sys.argv[0]).resolve().parent
	config_file = PREFIX.joinpath('config.ini').resolve()
	koef_x = {'left': 1, 'center': 1, 'right': -1}
	koef_y = {'top': 1, 'center': 1, 'bottom': -1}

	@staticmethod
	def CalcPositionX(pos_x: str, scr_width: int, width: int):
		''' Calculate Position Left (x) '''
		if PositionX.GetPosValue(pos_x) == PositionX.Left:
			calc_x = 15
		elif PositionX.GetPosValue(pos_x) == PositionX.Center:
			calc_x = int(scr_width/2) - int(width/2)
		else:
			calc_x = scr_width - width - 15
		return calc_x

	@staticmethod
	def CalcPositionY(pos_y: str, scr_height: int, height: int):
		''' Calculate Position Top (y) '''
		if PositionY.GetPosValue(pos_y) == PositionY.Top:
			calc_y = 15
		elif PositionY.GetPosValue(pos_y) == PositionY.Center:
			calc_y =  int(scr_height/2) - int(height/2)
		else:
			calc_y = scr_height - height - 30
		return calc_y

class Arguments:
	''' The class of the set of input parameters. '''
	
	__slots__ = ['Title', 'Message', 'OnTime', 'isTimer', 'icon', 
				'TitleFont_Family', 'TitleFont_Size',  'TitleFont_Weight', 
				'TitleFont_Underline', 'TitleFont_Slant', 'TitleFont_Overstrike', 
				'TitleBG', 'TitleFG', 
				'BodyFont_Family', 'BodyFont_Size', 'BodyFont_Weight', 
				'BodyFont_Underline', 'BodyFont_Slant', 'BodyFont_Overstrike',
				'BodyBG', 'BodyFG', 
				'Scale', 'PosX', 'PosY', 'Alpha', 'MoveX', 'MoveY', 'Relative', 
				'save', 'load', 'reset'
				]
	
	def __init__(self, *args, **kwargs):
		self.Title = args[0] if len(args) >= 1 else kwargs.get('Title','Apps')
		self.Message = args[1] if len(args) >= 2 else kwargs.get('Message','Info!')
		self.OnTime = args[2] if len(args) >= 3 else kwargs.get('OnTime',10000)
		self.isTimer = args[3] if len(args) >= 4 else kwargs.get('isTimer',True)
		self.icon = args[4] if len(args) >= 5 else kwargs.get('icon','')
		self.TitleFont_Family = args[5] if len(args) >= 6 else kwargs.get('TitleFont_Family','Arial')
		self.TitleFont_Size = args[6] if len(args) >= 7 else kwargs.get('TitleFont_Size',14)
		self.TitleFont_Weight = args[7] if len(args) >= 8 else kwargs.get('TitleFont_Weight','bold')
		self.TitleFont_Underline = args[8] if len(args) >= 9 else kwargs.get('TitleFont_Underline',0)
		self.TitleFont_Slant = args[9] if len(args) >= 10 else kwargs.get('TitleFont_Slant','roman')
		self.TitleFont_Overstrike = args[10] if len(args) >= 11 else kwargs.get('TitleFont_Overstrike',0)
		self.TitleBG = args[11] if len(args) >= 12 else kwargs.get('TitleBG','#FFFADD')
		self.TitleFG = args[12] if len(args) >= 13 else kwargs.get('TitleFG','black')
		self.BodyFont_Family = args[13] if len(args) >= 14 else kwargs.get('BodyFont_Family','Arial')
		self.BodyFont_Size = args[14] if len(args) >= 15 else kwargs.get('BodyFont_Size',14)
		self.BodyFont_Weight = args[15] if len(args) >= 16 else kwargs.get('BodyFont_Weight','normal')
		self.BodyFont_Underline = args[16] if len(args) >= 17 else kwargs.get('BodyFont_Underline',0)
		self.BodyFont_Slant = args[17] if len(args) >= 18 else kwargs.get('BodyFont_Slant','roman')
		self.BodyFont_Overstrike = args[18] if len(args) >= 19 else kwargs.get('BodyFont_Overstrike',0)
		self.BodyBG = args[19] if len(args) >= 20 else kwargs.get('BodyBG','#FFFADD')
		self.BodyFG = args[20] if len(args) >= 21 else kwargs.get('BodyFG','black')
		self.Scale = args[21] if len(args) >= 22 else kwargs.get('Scale', '1,1')
		self.PosX = args[22] if len(args) >= 23 else kwargs.get('PosX', 'right')
		self.PosY = args[23] if len(args) >= 24 else kwargs.get('PosY', 'top')
		self.Alpha = args[24] if len(args) >= 25 else kwargs.get('Alpha', 1.0)
		self.MoveX = args[25] if len(args) >= 26 else kwargs.get('MoveX', 0)
		self.MoveY = args[26] if len(args) >= 27 else kwargs.get('MoveY', 0)
		self.Relative = args[27] if len(args) >= 28 else kwargs.get('Relative', True)
	
	def __getattr__(self, attrname):
		''' Access to a non-existent variable. '''
		return None
	
	def __repr__(self):
		''' For Debug Function output paramters '''
		return f"{self.__class__}:" + \
				f"\n\tTitle = {self.Title}," + \
				f"\n\tText = {self.Message}," + \
				f"\n\tOnTime = {self.OnTime}," + \
				f"\n\tisTimer = {self.isTimer}," + \
				f"\n\ticon = {self.icon}," + \
				f"\n\tTitle Font Family = {self.TitleFont_Family}, Title Font size = {self.TitleFont_Size}," + \
				f"\n\tTitle Font Weight = {self.TitleFont_Weight}, Title Font Underline = {self.TitleFont_Underline}," + \
				f"\n\tTitle Font Slant: {self.TitleFont_Slant}, Title Font Overstrike = {self.TitleFont_Overstrike}," + \
				f"\n\tTitle BG = {self.TitleBG}, Title FG = {self.TitleFG}," + \
				f"\n\tBody BG = {self.BodyBG}, Body FG = {self.BodyFG}," + \
				f"\n\tBody Font Family = {self.BodyFont_Family}, Body Font Size = {self.BodyFont_Size}," + \
				f"\n\tBody Font Weight = {self.BodyFont_Weight}, Body Font Underline = {self.BodyFont_Underline}," + \
				f"\n\tBody Font Slant = {self.BodyFont_Slant}, Body Font Overstrike = {self.BodyFont_Overstrike}," + \
				f"\n\tScale = ({self.Scale})," + \
				f"\n\tPosX = {self.PosX}, PosY = {self.PosY}, MoveX = {self.MoveX}, MoveY = {self.MoveY}," + \
				f"\n\tTransparent (Alpha) = {self.Alpha}, Relative move position = {self.Relative}"

class Notify:
	''' Tkinter class form. '''
	
	def __init__(self, on_args: Arguments = Arguments()):
		''' Function init tkinter Apps '''
		self.args = on_args
		self.root = tk.Tk()
		
		self.TitleFont = fnt.Font(family = self.args.TitleFont_Family, size = self.args.TitleFont_Size, weight = self.args.TitleFont_Weight)
		self.TitleFont.configure(underline = self.args.TitleFont_Underline, slant = self.args.TitleFont_Slant, overstrike = self.args.TitleFont_Overstrike)
		
		self.BodyFont = fnt.Font(family = self.args.BidyFont_Family, size = self.args.BodyFont_Size, weight = self.args.BodyFont_Weight)
		self.BodyFont.configure(underline = self.args.BodyFont_Underline, slant = self.args.BodyFont_Slant, overstrike = self.args.BodyFont_Overstrike)
		
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
			self.root.after(self.args.OnTime, self.update_clock)
	
	def __FormTimer_Init(self):
		''' Timer on destroy form parameters and functions '''
		self.timer_flag = True
		self.on_time = self.args.OnTime
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
		if self.args.isTimer:
			self.update_clock()
		self.root.mainloop()
	
	def __CreateTitle(self):
		''' TKinter Title '''
		self.root.title(self.args.Title)
		self.root.configure(bg=self.args.BodyBG)
	
	def __CreateTransparent(self):
		''' Transparent Form parameters '''
		self.root.resizable(0,0)
		self.root.overrideredirect(1)
		self.root.wm_attributes("-topmost", 1)
		self.root.wait_visibility(self.root)
	
	def __CreateBtnClose(self):
		''' Create Button on Close '''
		self.close_icon = tk.PhotoImage(file = Defaults.PREFIX.joinpath('close-icon.png'))
		self.close_icon = self.close_icon.subsample(1, 1)
		self.btn1 = tk.Button(self.root, text="", justify=tk.CENTER,
						borderwidth=0,
						bg=self.args.TitleBG,
						fg=self.args.TitleFG,
						highlightcolor='white',
						activebackground='white',
						highlightthickness = 0,
						image=self.close_icon,
						command=self.root.destroy
						)
	
	def __CreateHeader(self):
		''' Create Header '''
		self.label_3 = tk.Label(self.root, text=self.args.Title,
							bg=self.args.TitleBG,
							fg=self.args.TitleFG,
							font=self.TitleFont,
							justify=tk.CENTER,
							padx=10,
							pady=0
							)

	def __CreateIcon(self):
		''' Crete Icon on forms (image) '''
		tmp_icon = pathlib.Path(self.args.icon).resolve()
		self.on_icon = str(tmp_icon) if tmp_icon.exists() else ''
		self.image = tk.PhotoImage(file=self.on_icon)
		self.image = self.image.subsample(*self.args.Scale.split(','))
		self.label_1 = tk.Label(self.root, text=f"",
							bg=self.args.BodyBG,
							fg=self.args.BodyFG,
							font=self.BodyFont,
							justify=tk.CENTER
							)
		self.label_1.image = self.image
		self.label_1['image'] = self.label_1.image
		
	def __CreateText(self):
		''' Create Text notify '''		
		if self.args.on_icon != '':
			self.label_2 = tk.Label(self.root, text=self.args.Message,
								bg=self.args.BodyBG,
								fg=self.args.BodyFG,
								font=self.BodyFont,
								justify=tk.CENTER
								)
		else:
			self.label_2 = tk.Label(self.root, text=self.args.Message,
								bg=self.args.BodyBG,
								fg=self.args.BodyFG,
								font=self.BodyFont,
								justify=tk.CENTER,
								padx=5,
								pady=0
								)
	
	def __ElementPack(self):
		''' Elements send (pack, place or grid standart class method) to Form '''
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
		
		if self.args.MoveX != 0 or self.args.MoveY != 0:
			if self.args.Relative:
				self.RelativePosition(self.args.MoveX, self.args.MoveY)
			else:
				self.RealPosition(self.args.MoveX, self.args.MoveY)
		
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
		position_x = self.args.PosX
		position_y = self.args.PosY
		Top = self.top
		Left = self.left
		Width = self.width
		Height = self.height

class Files:
	
	@staticmethod
	def WriteTextFile(on_text: str, on_file: str):
		''' Write data in text file '''
		with open(pathlib.Path(on_file).resolve(), "w") as fp:
			fp.write(on_text)
	
	@staticmethod
	def ReadTextFile(on_file: str) -> str:
		''' Read Data from text File '''
		on_text = ''
		with open(pathlib.Path(on_file).resolve(), "r") as fp:
			on_text = fp.read()
		return on_text
	
	@staticmethod
	def WriteJson(data_json: dict, file_json: str = 'object.json'):
		''' Write Json data in file '''
		with open(pathlib.Path(file_json).resolve(), "w") as fp:
			json.dump(data_json, fp, indent=2)

	@staticmethod
	def ReadJson(file_json: str = 'object.json') -> dict:
		''' Read Json Data from File '''
		data = ''
		with open(pathlib.Path(file_json).resolve(), "r") as fp:
			data = json.load(fp)
		return data

	@staticmethod
	def GetFileSuffix(List_Files, suffixes: str):
		''' Get for file suffix or extension file '''
		if List_Files != None:
			for x in List_Files:
				if suffixes == pathlib.Path(x).suffix:
					return pathlib.Path(x).resolve()
		return None

def CalcNewPosition(scr_width: int, scr_height: int, 
					pos_x: PositionX, pos_y: PositionY, 
					width: int, height: int, left: int, top: int):
	''' Calculation for new position to Form '''
	virt_x = width + 10
	virt_y = height + 10
	real_x = virt_x * Defaults.koef_x[pos_x.value] + left
	real_y = virt_y * Defaults.koef_y[pos_y.value] + top
	if pos_y == PositionY.Bottom:
		if real_y < 0:
			real_y = Defaults.CalcPositionY(pos_y, scr_height, height)
		else:
			real_x = left
	else:
		if (scr_height - real_y) < height:
			real_y = Defaults.CalcPositionY(pos_y, scr_height, height)
		else:
			real_x = left
	return real_x, real_y

def main():
	args = Arguments(icon='test1.png', Scale='2,2', Title='Title!', Message='Mesages to text output information!', OnTime=5000,
					PosX=PositionX.Right.value, PosY = PositionY.Top.value
					) # isTimer = True, MoveX = 100, MoveY = 100, Relative = False
	notification = Notify(args)
	'''
	global screen_width
	global screen_height
	global position_x
	global position_y
	global Width
	global Height
	global Left
	global Top
	'''
	notification.send()

if __name__ == '__main__':
	main()
