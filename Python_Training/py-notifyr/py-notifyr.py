#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import pathlib

class Window:
	
	def __init__(self, title: str = 'Apps', on_time: int = 10000,
				icon = '', fonts: tuple=('Arial', 14, 'bold'), 
				fg_color: str = 'black', bg_color: str = '#FFFADD', 
				text: str = 'Hello World!', 
				scale: tuple = (1, 1),
				alpha: float = 1.0, top: int = 0, left: int = 0):
		'''
			Function init tkinter Apps
		'''
		
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
							font=(fonts[0], fonts[1], fonts[2]),
							anchor='sw',
							justify=tk.CENTER
							)
		self.label_1.image = self.image
		self.label_1['image'] = self.label_1.image
		self.label_1.grid(row=1, column=0)
		
		# Text notify
		self.label_2 = tk.Label(self.root, text=text,
							bg=bg_color,
							fg=fg_color,
							font=(fonts[0], fonts[1], fonts[2]),
							anchor='sw',
							justify=tk.CENTER
							)
		self.label_2.grid(row=1, column=1)
		
		# Position Forms on Desktop: pos_x = Desktop.width - Form.Width - left; pos_y = 15 - top
		pos_width = self.root.winfo_screenwidth() - self.root.winfo_width() - 200 - left
		pos_height = 15 - top
		self.root.geometry()
		self.root.geometry(f"+{pos_width}+{pos_height}")
		self.root.minsize(100, 50)
		self.root.maxsize(640, 480)
		self.root.resizable(0,0)
		
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
	
	def update_clock(self):
		''' Timer on TKinter - finish to destroy application '''
		if not self.timer_flag:
			if self.count <= 0.1:
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

def main():
	icon_image = str(pathlib.Path('icon.png').resolve())
	win = Window(title = 'My App',
				icon = icon_image, fonts = ('Arial', 16, 'normal'), 
				fg_color = 'black', bg_color = '#FFFADD', 
				scale = (2, 2), text = "My Text!", 
				on_time = 5000, alpha = 1.0, top = 0, left = 0)

if __name__ == '__main__':
	main()
