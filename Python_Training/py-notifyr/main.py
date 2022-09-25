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

class Window:
	
	def __init__(self, title: str = 'Apps', on_time: int = 10000,
				icon = '', fonts: tuple=('Arial', 14, Weight.normal), 
				fg_color: str = 'black', bg_color: str = '#FFFADD', 
				text: str = 'Hello World!', 
				scale: tuple = (1, 1), width: int = 200, height: int = 100,
				pos_x: PositionX = PositionX.Right,
				pos_y: PositionY = PositionY.Top,
				alpha: float = 1.0, top: int = 0, left: int = 0):
		'''
			Function init tkinter Apps
		'''
		global screen_width
		global screen_height
		global position_x
		global position_y
		global worker_event
		global env_event
		worker_event.clear()
		env_event.clear()
		
		# TKinter Global
		self.root = tk.Tk()
		self.root.title(title)
		self.root.configure(bg=bg_color)
		
		# Transparent Form parameters
		self.root.resizable(0,0)
		#self.root.attributes(toolwindow=1)
		self.root.overrideredirect(1)
		self.root.wm_attributes("-topmost", 1)
		self.root.wait_visibility(self.root)
		
		# Button on Close
		self.close_icon = tk.PhotoImage(file = 'close-icon.png')
		self.close_icon = self.close_icon.subsample(1, 1)
		self.btn1 = tk.Button(text="", justify=tk.CENTER,
						borderwidth=0, 
						bg=bg_color,
						fg=fg_color,
						highlightcolor='white',
						activebackground='white',
						highlightthickness = 0,
						image=self.close_icon,
						command=self.root.destroy
						)
		self.btn1.grid(row=0, column=2)
		
		# Header
		self.label_3 = tk.Label(self.root, text=title,
							bg=bg_color,
							fg=fg_color,
							font=(fonts[0], fonts[1], 'bold'),
							anchor='sw',
							justify=tk.CENTER,
							padx=10,
							pady=0
							)
		self.label_3.grid(row=0, column=0)
		
		
		# Icon on forms (image)
		self.image = tk.PhotoImage(file=icon)
		self.image = self.image.subsample(*scale)
		self.label_1 = tk.Label(self.root, text=f"",
							bg=bg_color,
							fg=fg_color,
							font=(fonts[0], fonts[1], fonts[2].value),
							anchor='sw',
							justify=tk.CENTER
							)
		self.label_1.image = self.image
		self.label_1['image'] = self.label_1.image
		
		# Text notify
		self.label_2 = tk.Label(self.root, text=text,
							bg=bg_color,
							fg=fg_color,
							font=(fonts[0], fonts[1], fonts[2]),
							anchor='sw',
							justify=tk.CENTER
							)
		
		if icon != '':
			self.label_1.grid(row=1, column=0)
			self.label_2.grid(row=1, column=1)
		else:
			self.label_2.grid(row=1, column=0)
		
		# Position Forms on Desktop: pos_x = Desktop.width - Form.Width - left; pos_y = 15 - top
		# and Window size
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		pos_width = 0
		pos_height = 0
		self.width = width
		self.height = height
		self.root.geometry(f"{self.width}x{self.height}")
		if pos_x == PositionX.Right:
			pos_width = self.root.winfo_screenwidth() - self.width - 30 + left
			if pos_y == PositionY.Center:
				pos_height = int(self.root.winfo_screenheight()/2) - self.height + top
			if pos_y == PositionY.Top:
				pos_height = 15 + top
			if pos_y == PositionY.Bottom:
				pos_height = self.root.winfo_screenheight() - self.height - 30 + top
		if pos_x == PositionX.Center:
			pos_width = int(self.root.winfo_screenwidth()/2) - int(self.width/2) + left
			if pos_y == PositionY.Center:
				pos_height = int(self.root.winfo_screenheight()/2) - self.height + top
			if pos_y == PositionY.Top:
				pos_height = 15 + top
			if pos_y == PositionY.Bottom:
				pos_height = self.root.winfo_screenheight() - self.height - 30 + top
		if pos_x == PositionX.Left:
			pos_width = left + 30
			if pos_y == PositionY.Center:
				pos_height = int(self.root.winfo_screenheight()/2) - self.height + top
			if pos_y == PositionY.Top:
				pos_height = 15 + top
			if pos_y == PositionY.Bottom:
				pos_height = self.root.winfo_screenheight() - self.height - 30 + top
		self.root.geometry(f"+{pos_width}+{pos_height}")
		self.root.minsize(110, 70)
		self.root.maxsize(800, 600)
		self.root.resizable(0,0)
		
		position_x = pos_width
		position_y = pos_height
		env_event.set()
		
		# Show an opaque form when hovering over the mouse
		self.root.bind("<Enter>", self.on_enter)
		self.root.bind("<Leave>", self.on_leave)
		
		# Timer on destroy form parameters and functions
		self.timer_flag = True
		self.on_time = on_time
		self.counter = 0.1
		self.count = alpha
		self.update_clock()
		
		# Global Form LOOP - visibility
		self.root.mainloop()
		worker_event.set()
	
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

def BuildWindow(on_x: int, on_y: int, on_width: int, on_height: int):
	global Top
	global Left
	global worker_event
	worker_event.wait()
	icon_image = str(pathlib.Path('test1.png').resolve())
	win = Window(title = 'My App',
				icon = icon_image, fonts = ('Arial', 16, Weight.normal), 
				fg_color = 'black', bg_color = '#FFFADD', 
				scale = (2, 2), text = "My Text!", 
				pos_x = on_x, pos_y = on_y, width = on_width, height = on_height,
				on_time = 5000, alpha = 1.0, top = Top, left = Left)

def AppsConfig(pos_x: int, pos_y: int, on_width: int, on_height: int):
	global screen_width
	global screen_height
	global position_x
	global position_y
	global Top
	global Left
	global env_event
	global worker_event
	# getpid()
	# 1116 15
	pass

def main():
	on_pos_x = PositionX.Right
	on_pos_y = PositionY.Top
	w = 220
	h = 100
	top = 0
	left = 0
	thread_json_config = threading.Thread(target=AppsConfig, args=(on_pos_x, on_pos_y, w, h))
	#thread_win = threading.Thread(target=BuildWindow, args=(on_pos_x, on_pos_y, w, h))
	thread_json_config.start()
	#thread_win.start()
	#time.sleep(5)
	pass

if __name__ == '__main__':
	main()
