#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import pathlib

class Window:
	
	def __init__(self, title: str = 'Apps', height: int = 200, width: int = 100, on_time: int = 10000,
				logo = '', icon = '', fonts: tuple=('Arial', 14, 'bold'), text_color: str = 'black', scale: tuple = (1, 1), 
				text: str = 'Hello World!', top: int = 0, left: int = 0): # on_time: int = 10000
		self.on_time = on_time
		self.root = tk.Tk()
		self.root.title(title)
		
		photo = tk.PhotoImage(file = logo)
		self.root.wm_iconphoto(False, photo)
		
		self.image = tk.PhotoImage(file=icon)
		self.image = self.image.subsample(*scale)
		self.label_1 = tk.Label(self.root, text=f"",
							fg=text_color,
							font=(fonts[0], fonts[1], fonts[2]),
							anchor='sw',
							justify=tk.CENTER
							)
		
		self.label_1.image = self.image
		self.label_1['image'] = self.label_1.image
		self.label_1.grid(row=0, column=0)
		self.label_2 = tk.Label(self.root, text=text,
							fg=text_color,
							font=(fonts[0], fonts[1], fonts[2]),
							anchor='sw',
							justify=tk.CENTER
							)
		
		self.label_2.grid(row=0, column=1)
		
		pos_width = self.root.winfo_screenwidth() - width - 200 - left
		pos_height = 15 - top #win.winfo_screenheight() - height - 10
		self.root.geometry()
		self.root.geometry(f"+{pos_width}+{pos_height}")
		self.root.minsize(100, 50)
		self.root.maxsize(640, 480)
		self.root.resizable(0,0)
		
		self.root.wm_attributes("-topmost", 1)
		
		self.timer_flag = True
		self.counter = 0.1
		self.count = 1.0
		self.update_clock()
		
		self.root.wait_visibility(self.root)
		self.root.attributes('-alpha', 1.0)
		self.root.mainloop()
	
	def update_clock(self):
		if not self.timer_flag:
			if self.count <= 0.3:
				self.root.destroy()
			else:
				self.count = float(f"{(self.count - self.counter):.1f}")
				self.root.attributes('-alpha', self.count)
			self.root.after(100, self.update_clock)
		else:
			self.timer_flag = False
			self.root.after(self.on_time, self.update_clock)

def main():
	icon_logo = str(pathlib.Path('logo.png').resolve())
	icon_image = str(pathlib.Path('icon.png').resolve())
	win = Window(title = 'My App', width = 100, height = 200, 
				icon = icon_image, logo = icon_logo, fonts = ('Arial', 16, 'normal'), 
				text_color = 'black', scale = (2, 2), text = "My Text!", 
				on_time = 5000, top = 0, left = 0)

if __name__ == '__main__':
	main()
