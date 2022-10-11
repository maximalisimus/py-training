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

class Defaults:
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

	@staticmethod
	def CalcNewPosition(scr_width: int, scr_height: int, 
					pos_x: str, pos_y: str,  
					width: int, height: int, 
					left: int, top: int):
		''' Calculation for new position to Form '''
		virt_x = width + 10
		virt_y = height + 10
		real_x = virt_x * Defaults.koef_x[pos_x.value] + left
		real_y = virt_y * Defaults.koef_y[pos_y.value] + top
		if PositionY.GetPosValue(pos_y) == PositionY.Bottom:
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

class Arguments:
	''' The class of the set of input parameters. 
	
		Variables:
			Title: Header Text,
			Message: Text notify,
			OnTime: The waiting time before the form closes automatically,
			isTimer: The presence of a timer for automatically closing the application,
			icon: Icon to display inside the notification,
			TFFamily: Title Font Family,
			TFSize: Title Font size
			TFWeight: Title Font Weight (normal, bold), 
			TFUnderline: Title Font Underline (0, 1),
			TFSlant: Title Font Slant (italic, roman), 
			TFOverstrike: Title Font Overstrike (0, 1),
			TitleFG: Title Foreground Color (Header, Title Text Color),
			BG: Background Color, 
			BodyFG: Body Foreground Color (Message Text Color),
			BFFamily: Body Font Family, 
			BFSize: Body Font Size,
			BFWeight: Body Font Weight (normal, bold), 
			BFUnderline: Body Font Underline (0, 1),
			BFSlant: Body Font Slant (italic, roman), 
			BFOverstrike: Body Font Overstrike (0, 1),
			scale: The scale of the icon, 
					the value should be specified 
					as a string without spaces 
					(for example, "1,1" or "2,2"),
			PosX: The value of the X-axis position (left), 
				according to the "PositionX" class, 
			PosY: The value of the Y-axis position (top), 
					according to the "PositionY" class, 
			MoveX: Offset on the X-axis (Left), 
			MoveY: Offset on the Y-axis (Top),
			Alpha: Transparent (Alpha), 
			Relative: Relative move position (True, False),
			Topmost: On top of all windows (True, False),
			save: Save Configuration,
			load: Load configuration,
			reset: Reset the configuration,
			CloseIcon: Icon file for the form close button,
			ScaleClose: The scale of the Close icon, 
					the value should be specified 
					as a string without spaces 
					(for example, "1,1" or "2,2"),
			Theme: Theme, setting up form elements,
			input: Application Settings input file,
			output: The output file of the application settings,
			Style: Form style ("standart", "compact").
	'''
	
	__slots__ = ['Title', 'Message', 'OnTime', 'isTimer', 'icon', 
				'TFFamily', 'TFSize',  'TFWeight', 
				'TFUnderline', 'TFSlant', 'TFOverstrike', 
				'TitleFG', 'BG', 'BodyFG',
				'BFFamily', 'BFSize', 'BFWeight', 
				'BFUnderline', 'BFSlant', 'BFOverstrike', 
				'scale', 'PosX', 'PosY', 'Alpha', 'MoveX', 'MoveY', 'Relative', 'Topmost',
				'save', 'load', 'reset', 'CloseIcon', 'ScaleClose', 'Theme', 'input', 'output', 'Style'
				]
	
	def __init__(self, *args, **kwargs):
		self.Title = args[0] if len(args) >= 1 else kwargs.get('Title','Apps')
		self.Message = args[1] if len(args) >= 2 else kwargs.get('Message','Info!')
		self.OnTime = args[2] if len(args) >= 3 else kwargs.get('OnTime',10000)
		self.isTimer = args[3] if len(args) >= 4 else kwargs.get('isTimer',True)
		self.icon = args[4] if len(args) >= 5 else kwargs.get('icon','')
		self.TFFamily = args[5] if len(args) >= 6 else kwargs.get('TFFamily','Arial')
		self.TFSize = args[6] if len(args) >= 7 else kwargs.get('TFSize',14)
		self.TFWeight = args[7] if len(args) >= 8 else kwargs.get('TFWeight','bold')
		self.TFUnderline = args[8] if len(args) >= 9 else kwargs.get('TFUnderline',0)
		self.TFSlant = args[9] if len(args) >= 10 else kwargs.get('TFSlant','roman')
		self.TFOverstrike = args[10] if len(args) >= 11 else kwargs.get('TFOverstrike',0)
		self.TitleFG = args[11] if len(args) >= 12 else kwargs.get('TitleFG','black')
		self.BFFamily = args[12] if len(args) >= 13 else kwargs.get('BFFamily','Arial')
		self.BFSize = args[13] if len(args) >= 14 else kwargs.get('BFSize',14)
		self.BFWeight = args[14] if len(args) >= 15 else kwargs.get('BFWeight','normal')
		self.BFUnderline = args[15] if len(args) >= 16 else kwargs.get('BFUnderline',0)
		self.BFSlant = args[16] if len(args) >= 17 else kwargs.get('BFSlant','roman')
		self.BFOverstrike = args[17] if len(args) >= 18 else kwargs.get('BFOverstrike',0)
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
		self.input = args[33] if len(args) >= 34 else kwargs.get('input', '')
		self.output = args[34] if len(args) >= 35 else kwargs.get('output', '')
		self.Style = args[35] if len(args) >= 36 else kwargs.get('Style', 'standart')
		self.ScaleClose = args[36] if len(args) >= 37 else kwargs.get('ScaleClose', '1,1')
	
	def Reset(self):
		self.Title = 'Apps'
		self.Message = 'Info!'
		self.OnTime = 10000
		self.isTimer = True
		self.icon = ''
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
		self.input = ''
		self.output = ''
		self.Style = 'standart'
		self.ScaleClose = '1,1'
	
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
				f"\n\tTitle Font Family = {self.TFFamily}, Title Font size = {self.TFSize}," + \
				f"\n\tTitle Font Weight = {self.TFWeight}, Title Font Underline = {self.TFUnderline}," + \
				f"\n\tTitle Font Slant = {self.TFSlant}, Title Font Overstrike = {self.TFOverstrike}," + \
				f"\n\tTitle FG = {self.TitleFG}, Body FG = {self.BodyFG}, BG = {self.BG}," + \
				f"\n\tBody Font Family = {self.BFFamily}, Body Font Size = {self.BFSize}," + \
				f"\n\tBody Font Weight = {self.BFWeight}, Body Font Underline = {self.BFUnderline}," + \
				f"\n\tBody Font Slant = {self.BFSlant}, Body Font Overstrike = {self.BFOverstrike}," + \
				f"\n\tScale = ({self.scale})," + \
				f"\n\tPosX = {self.PosX}, PosY = {self.PosY}, MoveX = {self.MoveX}, MoveY = {self.MoveY}," + \
				f"\n\tTransparent (Alpha) = {self.Alpha}, Relative move position = {self.Relative}," + \
				f"\n\tTopmost = {self.Topmost}," + \
				f"\n\tSave = {self.save}, Load = {self.load}, Reset = {self.reset}," + \
				f"\n\tInput = {self.input}," + \
				f"\n\tOutput = {self.output}," + \
				f"\n\tStyle = {self.Style}," + \
				f"\n\tCloseIcon = {self.CloseIcon}," + \
				f"\n\tScaleClose = ({self.ScaleClose})"

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
		if self.args.Style == FormStyle.Standart.value:
			if self.args.CloseIcon == 'default':
				self.close_icon = tk.PhotoImage(file = Defaults.PREFIX.joinpath('exit_close.png'))
			else:
				self.close_icon = tk.PhotoImage(file = pathlib.Path(self.CloseIcon).resolve())
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
	
	def __CreateHeader(self):
		''' Create Header '''
		self.label_header = ttk.Label(self.root, text=self.args.Title, style='H.TLabel')
		self.label_header.bind('<Button-1>', self.__OnClose)

	def __CreateIcon(self):
		''' Crete Icon on forms (image) '''
		self.image = tk.PhotoImage(file=self.args.icon)
		self.image = self.image.subsample(*tuple(map(int, self.args.scale.split(','))))
		self.label_image = ttk.Label(self.root, text="", style='I.TLabel')
		self.label_image.bind('<Button-1>', self.__OnClose)
		self.label_image.image = self.image
		self.label_image['image'] = self.label_image.image
	
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
				self.label_header.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=0)
			else:
				self.label_header.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=0)
			self.btn1.grid(row=0, column=2)
			if self.args.icon != '':
				self.label_image.grid(row=1, column=0, padx=10, pady=0)
				self.label_text.grid(row=1, column=1, padx=0, pady=0)
			else:
				self.label_text.grid(row=1, column=0, padx=15, pady=0)
		else:
			if self.args.icon != '':
				for c in range(2):
					self.root.columnconfigure(index=c, weight=1)
				for r in range(2):
					self.root.rowconfigure(index=r, weight=1)
				self.label_image.grid(row=0, column=0, rowspan=2, sticky='w', padx=10, pady=0)
				self.label_header.grid(row=0, column=1, padx=0, pady=0, sticky='w')
				self.label_text.grid(row=1, column=1, padx=0, pady=0, sticky='w')
			else:
				for c in range(1):
					self.root.columnconfigure(index=c, weight=1)
				for r in range(2):
					self.root.rowconfigure(index=r, weight=1)
				self.label_header.grid(row=0, column=0, padx=10, pady=0, sticky='w')
				self.label_text.grid(row=1, column=0, padx=10, pady=0, sticky='w')
	
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
		''' Position Forms on Desktop '''
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
	'''  Class Files.
	
		Info: A class for working with files.
		
		Methods:
			WriteTextFile(data_text: str, text_file: str = 'text.txt'):
				Writing text to a text file.
			
			ReadTextFile(text_file: str = 'text.txt') -> dict:
				Reading text from a text file.
			
			WriteJson(data_json: dict, file_json: str = 'object.json'):
				Writing JSON data to a json file.
			
			ReadJson(file_json: str = 'object.json') -> dict:
				Reading JSON data from a json file.
			
			GetFileSuffix(List_Files, suffixes: str):
				Get a file with the specified extension from a list or tuple.
	'''
	
	@staticmethod
	def WriteTextFile(data_text: str, text_file: str = 'text.txt'):
		''' Write Text data in file '''
		with open(pathlib.Path(text_file).resolve(), "w") as fp:
			fp.write(data_text)

	@staticmethod
	def ReadTextFile(text_file: str = 'text.txt') -> dict:
		''' Read Text Data from File '''
		data = ''
		with open(pathlib.Path(text_file).resolve(), "r") as fp:
			data = fp.read()
		return data
	
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

def main():
	args = Arguments(icon='test1.png', scale='3,3', Title='Apps!', Message='Mesages to text output information!', OnTime=5000,
					PosX=PositionX.Right.value, PosY = PositionY.Top.value, isTimer = True, Topmost = False, Style = FormStyle.Standart.value
					)
	args.BG = '#303030'
	#args.BG = '#E1E1E1'
	#args.TitleFG = 'green'
	#args.BodyFG = 'blue'
	#args.BFUnderline = 1
	#args.TFOverstrike = 1
	args.TitleFG = 'white'
	args.BodyFG = 'white'
	args.Alpha = 0.9
	#args.icon = ''
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
