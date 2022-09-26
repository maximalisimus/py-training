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
	def GetWeight(cls, weight: str):
		for x in cls:
			if weight == x.value:
				return x
		return None

class PositionX(NoValue):
	Left = 'left'
	Right = 'right'
	Center = 'center'
	
	@classmethod
	def GetPos(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

class PositionY(NoValue):
	Top = 'top'
	Center = 'center'
	Bottom = 'Bottom'

	@classmethod
	def GetPos(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

class Arguments:
	
	__slots__ = 'title text on_time icon fonts fg_color bg_color scale width height pos_x pos_y alpha top left'.split()
	
	def __init__(self, *args, **kwargs):
		self.title = args[0] if len(args) >= 1 else kwargs.get('title', 'Apps')
		self.text = args[1] if len(args) >= 2 else kwargs.get('text', 'Ok!')
		self.on_time = args[2] if len(args) >= 3 else kwargs.get('on_time', 10000)
		self.icon = pathlib.Path(args[3]).resolve() if len(args) >= 4 else kwargs.get('icon', '')
		self.fonts = list(str(args[4]).split(',')) if len(args) >= 5 else list(str(kwargs.get('fonts','Arial,14,normal')).split(','))
		self.fonts[1] = int(self.fonts[1])
		self.fonts[2] = Weight.GetWeight(self.fonts[2])
		self.fonts = tuple(self.fonts)
		self.fg_color = args[5] if len(args) >= 6 else kwargs.get('fg_color', 'black')
		self.bg_color = args[6] if len(args) >= 7 else kwargs.get('bg_color', '#FFFADD')
		self.scale = tuple(map(int, str(args[7]).split(',')))  if len(args) >= 8 else tuple(map(int, str(kwargs.get('scale', '1,1')).split(',')))
		self.width = args[8] if len(args) >= 9 else kwargs.get('width', 200)
		self.height = args[9] if len(args) >= 10 else kwargs.get('height', 100)
		self.pos_x = PositionX.GetPos(args[10]) if len(args) >= 11 else PositionX.GetPos(kwargs.get('pos_x', 'right'))
		self.pos_y = PositionY.GetPos(args[11]) if len(args) >= 12 else PositionY.GetPos(kwargs.get('pos_y', 'top'))
		self.alpha = args[12] if len(args) >= 13 else kwargs.get('alpha', 1.0)
		self.top = args[13] if len(args) >= 14 else kwargs.get('top', 0)
		self.left = args[14] if len(args) >= 15 else kwargs.get('left', 0)
	
	def __getattr__(self, attrname):
		return None
	
	def __repr__(self):
		return f"{self.__class__}:" + \
				f"\n\tTitle: {self.title}" + \
				f"\n\tText: {self.text}" + \
				f",\n\tTime: {self.on_time} ms" + \
				f",\n\tIcon: {self.icon if self.icon != '' else None}," + \
				f"\n\tFonts: {self.fonts}," + \
				f"\n\tFG Color: {self.fg_color}, " + \
				f"BG Color: {self.bg_color}, " + \
				f"\n\tScale: {self.scale}, width: {self.width}, height: {self.height}," + \
				f"\n\tPos X: {self.pos_x}, Pos Y: {self.pos_y}," + \
				f"\n\tAlpha: {self.alpha}," + \
				f"\n\tTop: {self.top}, Left: {self.left}"

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
		self.__CreatePosition()
		
		# Show an opaque form when hovering over the mouse
		self.root.bind("<Enter>", self.on_enter)
		self.root.bind("<Leave>", self.on_leave)
		
		self.__FormTimer_Init()
	
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
			self.root.after(self.on_time, self.update_clock)
	
	def on_enter(self, event):
		''' Form focused '''
		self.root.attributes('-alpha', 1.0)
	
	def on_leave(self, enter):
		''' Form not focused '''
		self.root.attributes('-alpha', self.count)
	
	def __CreateTitle(self):
		''' TKinter Title '''
		self.root.title(self.args.title)
		self.root.configure(bg=self.args.bg_color)
	
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
		self.btn1 = tk.Button(text="", justify=tk.CENTER,
						borderwidth=0, 
						bg=self.args.bg_color,
						fg=self.args.fg_color,
						highlightcolor='white',
						activebackground='white',
						highlightthickness = 0,
						image=self.close_icon,
						command=self.root.destroy
						)
		self.btn1.grid(row=0, column=2)
	
	def __CreateHeader(self):
		''' Header '''
		self.label_3 = tk.Label(self.root, text=self.args.title,
							bg=self.args.bg_color,
							fg=self.args.fg_color,
							font=(self.args.fonts[0], self.args.fonts[1], 'bold'),
							anchor='sw',
							justify=tk.CENTER,
							padx=10,
							pady=0
							)
		self.label_3.grid(row=0, column=0)

	def __CreateIcon(self):
		''' Icon on forms (image) '''
		self.image = tk.PhotoImage(file=self.args.icon)
		self.image = self.image.subsample(*self.args.scale)
		self.label_1 = tk.Label(self.root, text=f"",
							bg=self.args.bg_color,
							fg=self.args.fg_color,
							font=(self.args.fonts[0], self.args.fonts[1], self.args.fonts[2].value),
							anchor='sw',
							justify=tk.CENTER
							)
		self.label_1.image = self.image
		self.label_1['image'] = self.label_1.image
	
	def __CreateText(self):
		''' Text notify '''
		self.label_2 = tk.Label(self.root, text=self.args.text,
							bg=self.args.bg_color,
							fg=self.args.fg_color,
							font=(self.args.fonts[0], self.args.fonts[1], self.args.fonts[2]),
							anchor='sw',
							justify=tk.CENTER
							)
		
		if self.args.icon != '':
			self.label_1.grid(row=1, column=0)
			self.label_2.grid(row=1, column=1)
		else:
			self.label_2.grid(row=1, column=0)

	def __CreatePosition(self):
		''' 
			Position Forms on Desktop: pos_x = Desktop.width - Form.Width - left; pos_y = 15 - top 
			and Window size
		'''
		self.screen_width = self.root.winfo_screenwidth()
		self.screen_height = self.root.winfo_screenheight()
		pos_width = 0
		pos_height = 0
		self.root.geometry(f"{self.args.width}x{self.args.height}")
		if self.args.pos_x == PositionX.Right:
			pos_width = self.root.winfo_screenwidth() - self.args.width - 30 + self.args.left
			if self.args.pos_y == PositionY.Center:
				pos_height = int(self.root.winfo_screenheight()/2) - self.args.height + self.args.top
			if self.args.pos_y == PositionY.Top:
				pos_height = 15 + self.args.top
			if self.args.pos_y == PositionY.Bottom:
				pos_height = self.root.winfo_screenheight() - self.args.height - 30 + self.args.top
		if self.args.pos_x == PositionX.Center:
			pos_width = int(self.root.winfo_screenwidth()/2) - int(self.args.width/2) + self.args.left
			if pos_y == PositionY.Center:
				pos_height = int(self.root.winfo_screenheight()/2) - self.args.height + self.args.top
			if self.args.pos_y == PositionY.Top:
				pos_height = 15 + self.args.top
			if self.args.pos_y == PositionY.Bottom:
				pos_height = self.root.winfo_screenheight() - self.args.height - 30 + self.args.top
		if self.args.pos_x == PositionX.Left:
			pos_width = self.args.left + 30
			if self.args.pos_y == PositionY.Center:
				pos_height = int(self.root.winfo_screenheight()/2) - self.args.height + self.args.top
			if self.args.pos_y == PositionY.Top:
				pos_height = 15 + top
			if self.args.pos_y == PositionY.Bottom:
				pos_height = self.root.winfo_screenheight() - self.args.height - 30 + self.args.top
		self.root.geometry(f"+{pos_width}+{pos_height}")
		self.root.minsize(110, 70)
		self.root.maxsize(800, 600)
		self.root.resizable(0,0)
		self.position_x = pos_width
		self.position_y = pos_height		
		global screen_width
		global screen_height
		global position_x
		global position_y
		global Top
		global Left
		screen_width = self.screen_width
		screen_height = self.screen_height
		position_x = pos_width
		position_y = pos_height
		Top = self.args.top
		Left = self.args.left

	def __FormTimer_Init(self):
		''' Timer on destroy form parameters and functions '''
		self.timer_flag = True
		self.on_time = self.args.on_time
		self.counter = 0.1
		self.count = self.args.alpha
		self.update_clock()
	
	def Run(self):
		''' Global Form LOOP - visibility '''
		self.root.mainloop()

class Defaults:
	
	PREFIX = pathlib.Path(sys.argv[0]).resolve().parent
	config_file = PREFIX.joinpath('config.ini').resolve()
	
	@staticmethod
	def GetDefaultData() -> dict:
		return {
				'screen_width': '1366',
				'scree_height': '768',
				'pos_x': f"{PositionX.Right.value}",
				'pos_y': f"{PositionY.Top.value}",
				'x': f"0",
				'y': f"0",
				'width': f"110",
				'height': f"70"
				}
	
	@staticmethod
	def GetDefaultWorker() -> dict:
		return {'unlock': True}

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
	'''
	global screen_width
	global screen_height
	global position_x
	global position_y
	global Top
	global Left
	'''
	win = Window()
	win.Run()
	pass

if __name__ == '__main__':
	main()
