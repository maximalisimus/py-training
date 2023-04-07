#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A program for downloading SSL certificates (domain, root and intermediate centers) to different files on a PC.

Artamonov Mikhail [https://github.com/maximalisimus]
maximalis171091@yandex.ru
# License: GPL3
"""

__author__ = 'Mikhail Artamonov'

try:
	from .version import version, progname
except ImportError:
	version = "1.0.0"
	progname = 'receive-cert'

__version__ = version

# $ pyinstaller --onefile --icon=apps.ico --paths version.py receive-cert.py

import sys
import os
import re
import pathlib
import platform
import tkinter as tk
from tkinter import ttk
import sys

class MyForm:
	def __init__(self, master):
		self.master = master
		# получаем размеры экрана
		self.width_screen = self.master.winfo_screenwidth() 
		self.height_screen = self.master.winfo_screenheight()
		
		# задаем размеры окна и расположение по середине экрана
		self.width_window = int(self.width_screen*0.3)
		self.height_window = int(self.height_screen*0.3)
		self.x = int((self.width_screen/2) - (self.width_window/2))
		self.y = int((self.height_screen/2) - (self.height_window/2))
		self.master.geometry(f"{self.width_window}x{self.height_window}+{self.x}+{self.y}")
		
		# задаем название окна и иконку
		self.master.title("Загрузка SSL сертификатов")
		self.icon_file = pathlib.Path('./icon.png').resolve()
		if self.icon_file.exists():
			self.icon = tk.PhotoImage(file=str(self.icon_file))
			self.master.iconphoto(True, self.icon)

		self.frame = ttk.Frame(self.master, padding=20)
		self.frame.pack(expand=True)
		self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(2, weight=1)
		
		# создаем текстовое поле
		
		# создаем кнопку
		self.entry = ttk.Entry(self.frame, width=30)
		self.entry.grid(row=0, column=0, pady=15, padx=(0, 15), sticky="w")

		# создаем кнопку
		self.button = ttk.Button(self.frame, text="ОК", command=self.on_button_click)
		self.button.grid(row=0, column=1, pady=15, padx=(15, 0), sticky="e")
		
	def on_button_click(self):
		# получаем текст из поля для ввода
		self.text = self.entry.get()
		if not hasattr(self, 'text'):
			self.text = ''
		# закрываем окно и выводим сообщение с текстом
		self.master.destroy()
		#messagebox.showinfo("Сообщение", text)

def main():
	root = tk.Tk()
	my_form = MyForm(root)
	root.mainloop()
	if not hasattr(my_form, 'text'):
		sys.exit(0)
	if my_form.text == '':
		sys.exit(0)
	
	site = my_form.text
	website = site.replace('http://','').replace('https://','').split('/')[0].split('\\')[0]
	
	if platform.system() == 'Linux':
		command = f"openssl s_client -showcerts -connect {website}:443 </dev/null > ./certificate.txt"
	else:
		command = f"openssl s_client -showcerts -connect {website}:443 > ./certificate.txt"
	
	os.system(command)
	
	cert_file = pathlib.Path('./certificate.txt').resolve()
	with open(cert_file, "r") as f:
		lines = f.readlines()
	
	cert_file.unlink(missing_ok=True)
	
	root = pathlib.Path(f"{website}").resolve()
	root.mkdir(parents=True)
	
	onsearch1 = 's:C'
	onsearch2 = 'CN = '
	onsearch3 = 'BEGIN CERTIFICATE'
	onsearch4 = 'END CERTIFICATE'
	fname = ''
	outname = ''
	startname = True
	startcert = False
	endcert = False
	iswrite = False
	
	for item in lines:
		if onsearch1 in item and startname:
			onstart = re.search(onsearch2, item).end()
			fname = item[onstart:].replace('*','_')
			startname = False
			outname = str(fname  + '.crt').replace(onsearch2,'').replace('*','_').replace(' ','_').replace('\n','')
			outname = root.joinpath(outname.replace(' ','_')).resolve()
			iswrite = True
		elif onsearch1 in item:
			onstart = re.search(onsearch2, item).end()
			outname = str(fname + ' ' + item[onstart:]  + '.crt').replace(onsearch2,'').replace('*','_').replace(' ','_').replace('\n','')
			outname = root.joinpath(outname).resolve()
			iswrite = True
		if iswrite:
			with open(outname, 'a') as f:
				if onsearch3 in item:
					startcert = True
				if onsearch4 in item:
					startcert = False
					endcert = True
				if startcert:
					f.write(item)
				if endcert:
					endcert = False
					f.write(item)

if __name__ == '__main__':
	main()
