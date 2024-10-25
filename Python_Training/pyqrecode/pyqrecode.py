#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import qrcode
from PIL import Image
import sys
import pathlib
import argparse

# python -m pip install pip setuptools virtualenv virtualenvwrapper-win --upgrade pip setuptools virtualenv virtualenvwrapper-win

#Debian: $ sudo apt install python-virtualenv python3-virtualenv python3-venv virtualenv python3-virtualenvwrapper python-distlib python-filelock python3-platformdirs python-stevedore
#Archlinux: $ sudo pacman -S python-distlib python-filelock python-platformdirs python-stevedore python-virtualenv python-virtualenvwrapper
#Python PIP: $ python -m pip install --upgrade pip setuptools distlib filelock platformdirs stevedore virtualenv virtualenvwrapper --upgrade
#Windows PIP / PIP: $ pip install setuptools virtualenv virtualenvwrapper-win --upgrade

# pip install qrcode pillow pyinstaller

# --onefile — сборка в один файл, т.е. файлы .dll не пишутся.
# --windowed -при запуске приложения, будет появляться консоль.
# --noconsole — при запуске приложения, консоль появляться не будет.
# --icon=app.ico — добавляем иконку в окно.
# --paths — возможность вручную прописать путь к необходимым файлам, если pyinstaller
# не может их найти(например: --paths D:\python35\Lib\site-packages\PyQt5\Qt\bin)

# $ pyinstaller --onefile --icon=apps.ico pyqrecode.py

__author__ = 'Mikhail Artamonov'
__description__ = 'Text to QR code converter program.'
__progname__ = str(pathlib.Path(sys.argv[0]).resolve().name)
__copyright__ = f"© The \"{__progname__}\". Copyright  by 2024."
__credits__ = ["Mikhail Artamonov"]
__license__ = "Open Source"
__version__ = "1.0.0"
__maintainer__ = "Mikhail Artamonov"
__status__ = "Production"
__date__ = '24.10.2024'
__modifed__ = '25.10.2024'

class Author:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__author__}"

class Copyright:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__copyright__}"

class Сredits:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__credits__}"

class License:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__license__}"

class Maintainer:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__maintainer__}"

class Status:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__status__}"

class DateStart:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__date__}"

class DateModifed:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__modifed__}"

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

class Prog_Dir:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return str(pathlib.Path(__progname__).resolve().parent)

class Descriptions:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__description__}"

class Versions:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"{__version__}"

class Prog:
	
	author = Author()
	name = Prog_Name()
	full = Full_Prog()
	dirs = Prog_Dir()
	desc = Descriptions()
	vers = Versions()
	copyrights = Copyright()
	oncredits = Сredits()
	licenses = License()
	maintainer = Maintainer()
	status = Status()
	datestart = DateStart()
	datemodif = DateModifed()

class AuthorInfo:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"Author: {Prog.author}\nProgname: {Prog.name}\nVersion: {Prog.vers}\n" + \
			f"Description: {Prog.desc}\n" +\
			f"Date of creation: {Prog.datestart}\nLast modified date: {Prog.datemodif}\n" + \
			f"License: {Prog.licenses}\nCopyright: {Prog.copyrights}\nCredits: {Prog.oncredits}\n" + \
			f"Maintainer: {Prog.maintainer}\nStatus: {Prog.status}\n"

class Author:
	
	info = AuthorInfo()
	
	def __repr__(self):
		return f"{self.__class__}: {self.Info}"
	
	def __str__(self):
		return f"{self.Info}"
	
	def __call__(self):
		return f"{self.Info}"

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
	
	def __getattr__(self, attrname):
		''' Access to a non-existent variable. '''
		return None

def createParser(argv):
	
	dict_parser = dict()
	parser = argparse.ArgumentParser(prog=Prog.name, description=Prog.desc)
	parser.add_argument ('-v', '--version', action='version', version=f'{Prog.name} {Prog.vers}',  help='show version programm')
	parser.add_argument ('-i', '--info', action='store_true', default=False, help='detailed product information')
	parser.add_argument("-d", '--dirs', dest="dirs", metavar='DIRS', type=str, default=str(Prog.dirs), help='work directory')
	parser.add_argument("-o", '--output', dest="output", metavar='OUTPUT', type=str, default='image.png', help='output fule name (default: image.png)')
	parser.add_argument("-t", '--text', dest="text", metavar='TEXT', type=str, default='', help='text that needs to be encrypted into a QR code')
	parser.add_argument ('-s', '--show', action='store_true', default=False, help='open image with final qr code')
	
	dict_parser['parser'] = parser
	return dict_parser

def main(*argv):
	
	args = Arguments()
	parser_dict = createParser(args)
	
	if len(argv) > 0:
		parser_dict['parser'].parse_args(args=argv, namespace=Arguments)
	else:
		parser_dict['parser'].parse_args(namespace=Arguments)
	
	output_filename = str(pathlib.Path(args.dirs).resolve().joinpath(f"{args.output.split('.')[0]}.png"))
	
	if args.info:
		print(Author.info)
		sys.exit(0)
	
	if args.text != '':
		qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
		qr.add_data(str(args.text))
		qr.make(fit=True)
		img = qr.make_image(fill_color="black", back_color="white")
		img.save(output_filename)
		if args.show:
			im = Image.open(output_filename)
			im.show()
		sys.exit(0)
	else:		
		parser_dict['parser'].parse_args(['-h'])
		sys.exit(0)
	
	'''
	if len(sys.argv) > 2:
		output = str(pathlib.Path(sys.argv[0]).resolve().parent.joinpath(str(sys.argv[1])))
		
		qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
		qr.add_data(str(sys.argv[2]))
		qr.make(fit=True)
		img = qr.make_image(fill_color="black", back_color="white")
		img.save(output)
		
		im = Image.open(output)
		im.show()
	'''
	
if __name__ == '__main__':
	main()
